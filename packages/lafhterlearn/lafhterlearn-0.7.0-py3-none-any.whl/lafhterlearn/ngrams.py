import itertools
import os
import bisect
from collections import abc

import h5py
from nltk.util import ngrams
import numpy as np
from .ngram_utils import build_vocab, get_word_stream, SparseArray, backoff
from .formatters import show_progress_bar


def build_ngram_model(get_corpus, output_file, n):
    """Count ngrams and create count tables"""

    vocab = list(build_vocab(get_word_stream(get_corpus, n)))
    word2int = {word: i for i, word in enumerate(vocab)}

    with h5py.File(output_file, mode='w') as f:
        f.create_dataset("vocab", data=vocab)

        unigram_counts = build_unigram_counts(get_corpus, word2int)

        f.create_dataset(f'{1}-grams', data=unigram_counts)

        for order in range(2, n + 1):
            group = f.create_group(f'{order}-grams')
            group.attrs['order'] = order
            build_ngram_counts(get_corpus, group, word2int, n=order)


def build_unigram_counts(get_corpus, word2int):
    counts = np.zeros(len(word2int), dtype=int)

    for word in get_word_stream(get_corpus, 1):
        token = word2int.get(word, word2int['<UNK>'])
        counts[token] += 1
    return counts


def build_ngram_counts(get_corpus, h5group, word2int, n):
    tokens = (word2int.get(word, word2int['<UNK>'])
              for word in get_word_stream(get_corpus, n))

    ngrams_with_counts = sorted_ngram_counts(tokens, n)

    context_group = h5group.create_group('contexts')
    address_group = h5group.create_group('addresses')
    count_group = h5group.create_group('counts')

    gen_with_progress = show_progress_bar(data_to_write(ngrams_with_counts),
                                          desc='Progress: ')

    for chunk_number, chunk in enumerate(chunks(gen_with_progress, 1024 * 100)):
        contexts = []
        addresses = []
        counts = []
        for context, address, chunk_counts in chunk:
            contexts.append(context)
            addresses.append(address)
            for c in chunk_counts:
                counts.append(c)

        context_group.create_dataset(f'chunk_{chunk_number}', data=contexts)
        address_group.create_dataset(f'chunk_{chunk_number}', data=addresses)
        count_group.create_dataset(f'chunk_{chunk_number}', data=counts)


class CountTable:
    def __init__(self, h5group):
        self.h5group = h5group

        context_group = h5group['contexts']
        address_group = h5group['addresses']
        count_group = h5group['counts']

        self.contexts = load_2d_matrix(context_group)
        self.addresses = load_2d_matrix(address_group)
        self.counts = load_2d_matrix(count_group)

    def get_counts(self, context):
        context = tuple(context)
        idx = bisect.bisect_left(self.contexts, context)
        if self.contexts[idx] != context:
            raise ValueError(f'cannot find counts for context {context}')

        start, end = self.addresses[idx]
        return self.counts[start:end]


class NgramModel:
    class ProbabilityDistribution:
        def __init__(self, counts_array):
            self.counts_array = counts_array
            self.pmf = counts_array / counts_array.sum()
            self.rng = np.random.default_rng()

        def sample(self):
            return self.rng.choice(len(self.pmf), 1, p=self.pmf)[0]

    def __init__(self, count_tables, vocab):
        self.count_tables = count_tables
        self.vocab = vocab
        self.word2id = {word: i for i, word in enumerate(self.vocab)}

        unigram_counts = self.count_tables[1]
        self.unigram_dist = unigram_counts / sum(unigram_counts)

    def tokenize(self, word):
        if word not in self.word2id:
            word = '<UNK>'
        return self.word2id[word]

    def lookup_word(self, word_id):
        try:
            return self.vocab[word_id]
        except IndexError:
            return '<UNK>'

    def p_next(self, context):
        order = len(context) + 1

        prob_dists = []
        for i in range(order, 1, -1):
            count_table = self.count_tables[i]
            try:
                counts = count_table.get_counts(context)
            except ValueError:
                dist = np.zeros(len(self.vocab), dtype=np.float32)
                prob_dists.append(dist)
            else:
                a = np.zeros(len(self.vocab), dtype=np.int32)
                indices = counts[:, 0]
                values = counts[:, 1]
                a[indices] = values

                dist = a / a.sum()
                prob_dists.append(dist)

            context = context[1:]

        prob_dists.append(self.unigram_dist)
        pseudo_probs = backoff(*prob_dists)
        return self.ProbabilityDistribution(pseudo_probs)

    def generate(self, num_words):
        start_token = self.tokenize('<s>')
        max_order = len(self.count_tables) - 1
        context = tuple(start_token for _ in range(max_order))

        output = []
        for i in range(num_words):
            p = self.p_next(context)
            word_idx = p.sample()
            word = self.lookup_word(word_idx)
            context = context[1:] + (word_idx, )

            output.append(word)

        return output

    @classmethod
    def from_h5file(cls, f):
        unigram_counts = f["1-grams"][:]  # load array into memory

        def get_order(name):
            return int(name.split('-')[0])

        names = sorted([k for k in f.keys() if k not in ['1-grams', 'vocab']],
                       key=get_order)

        count_tables = {
            1: unigram_counts
        }
        for name in names:
            order = get_order(name)
            group = f[name]
            count_tables[order] = CountTable(group)

        vocab = [str(word) for word in f['vocab'].asstr()]
        return cls(count_tables, vocab)


class ModelProxy:
    def __init__(self, path):
        with h5py.File(path) as f:
            self.path = path
            self.unigram_counts = f["1-grams"][:]  # load array into memory

            def get_order(name):
                return int(name.split('-')[0])

            names = sorted([k for k in f.keys() if k not in ['1-grams', 'vocab']],
                           key=get_order)

            self.names_with_orders = [(name, get_order(name)) for name in names]
            self.vocab = [str(word) for word in f['vocab'].asstr()]

    def generate(self, num_words):
        with h5py.File(self.path) as f:
            count_tables = {
                1: self.unigram_counts
            }
            for name, order in self.names_with_orders:
                group = f[name]
                count_tables[order] = CountTable(group)

            model = NgramModel(count_tables, self.vocab)
            return model.generate(num_words)


def load_2d_matrix(h5group):
    def parse_chunk_number(name):
        _, number = name.split('_')
        return int(number)

    seqs = []
    for k in sorted(h5group.keys(), key=parse_chunk_number):
        seqs.append(h5group[k])

    return ChainSequence(*seqs)


class ChainSequence:
    """Read-only super sequence composed of individual sequences"""
    def __init__(self, *seqs):
        seqs = [s for s in seqs if s]
        self.seqs = seqs

        lengths = [len(s) for s in seqs]
        cum_lengths = list(itertools.accumulate(lengths, initial=0))
        self.intervals = list(zip(cum_lengths[:-1], cum_lengths[1:]))

        self.ends = [b for a, b in self.intervals]

    def __getitem__(self, idx):
        if isinstance(idx, int):
            return self.get_item(idx)
        elif isinstance(idx, abc.Sequence):
            raise ValueError(f'expects either integer index or slice. Got {idx}')
        elif isinstance(idx, slice):
            return self.get_slice(idx)

    def __len__(self):
        return sum(len(s) for s in self.seqs)

    def get_slice(self, index_slice):
        start = index_slice.start
        stop = index_slice.stop

        if start is None:
            first_ivl_index = 0
            first_offset = 0
        else:
            first_ivl_index, first_offset = self.locate_index(start)

        if stop is None or self.locate_index(stop) is None:
            last_ivl_index = len(self.intervals) - 1
            stop_offset = len(self.seqs[last_ivl_index])
        else:
            last_ivl_index, stop_offset = self.locate_index(stop)

        if first_ivl_index == last_ivl_index:
            seq = self.seqs[first_ivl_index]
            res = seq[first_offset:stop_offset]
        else:
            first_seq = self.seqs[first_ivl_index]
            res = first_seq[first_offset:]
            for i in range(first_ivl_index + 1, last_ivl_index):
                seq = self.seqs[i]
                res.extend(seq[:])

            last_seq = self.seqs[last_ivl_index]
            res.extend(last_seq[:stop_offset])

        return res

    def get_item(self, idx):
        if not (0 <= idx < len(self)):
            raise IndexError()

        ivl_index, offset = self.locate_index(idx)
        seq = self.seqs[ivl_index]
        # todo: dont normalize, let the client opportunity to interpret the type
        return normalize(seq[offset])

    def locate_index(self, idx):
        return self._fast_locate(idx)

    def _fast_locate(self, idx):
        endpoint_index = bisect.bisect_left(self.ends, idx)
        try:
            if self.ends[endpoint_index] == idx:
                ivl_index = endpoint_index + 1
            else:
                ivl_index = endpoint_index

            a, b = self.intervals[ivl_index]
            offset = idx - a
            return ivl_index, offset
        except IndexError:
            return None


def data_to_write(ngrams_with_counts):
    pos = 0
    for context, sparse_array in group_by_contexts(ngrams_with_counts):
        start = pos
        end = pos + len(sparse_array)
        address = (start, end)
        pos += len(sparse_array)
        yield context, address, sparse_array


def group_by_contexts(ngrams_with_counts):
    groups = itertools.groupby(ngrams_with_counts, key=lambda t: t[0][:-1])

    for context, grouper in groups:
        counts = []
        for ngram, count in grouper:
            token = ngram[-1]
            counts.append((token, count))
        yield context, counts


def sorted_ngram_counts(tokens, n):
    sorted_ngrams = bigsort(ngrams(tokens, n))

    if os.path.isfile("chunks.h5"):
        os.remove("chunks.h5")

    for ngram, grouper in itertools.groupby(sorted_ngrams):
        yield ngram, len(list(grouper))


def bigsort(iterable, chunk_size=1024 * 100, temp_file="chunks.h5"):
    """Sort large collection of data that may not fit in memory.
    Generates and yields items in ascending order.
    """

    with h5py.File(temp_file, "a") as f:
        for i, chunk in enumerate(sorted_chunks(iterable, chunk_size)):
            f.create_dataset(f'chunk_{i}', data=list(chunk))

        datasets = [serializable_ds(f[ds_name]) for ds_name in f.keys()]
        yield from merge_chunks(*datasets)


def serializable_ds(ds):
    for item in ds:
        yield normalize(item)


def normalize(item):
    if isinstance(item, np.int64):
        item = int(item)
    elif isinstance(item, int):
        item = int(item)
    else:
        item = tuple(item)

    return item


def chunks(iterable, size):
    if size <= 0:
        raise ValueError(f'chunk size has to be positive integer, got {size}')

    s = []
    for item in iterable:
        s.append(item)

        if len(s) == size:
            yield s
            s = []

    if s:
        yield s


def sorted_chunks(iterable, size):
    for chunk in chunks(iterable, size):
        yield sorted(chunk)


def merge_chunks(*iterables):
    iterators = []
    items = []

    for it in iterables:
        iterator = iter(it)

        try:
            item = next(iterator)
            iterators.append(iterator)
            items.append(item)
        except StopIteration:
            pass

    while items:
        smallest = min(items)
        yield smallest

        iterator_index = items.index(smallest)
        try:
            items[iterator_index] = next(iterators[iterator_index])
        except StopIteration:
            iterators.pop(iterator_index)
            items.pop(iterator_index)
