import numpy as np

# Filtering the item knowledge graph
def filterKG():
    file = '../data/item_kg.txt'
    writer = open('../data/item_kg_filtered.txt', 'w', encoding='utf-8')
    for line in open(file, encoding='utf-8').readlines():
        array = line.strip().split('\t')
        if int(array[0]) <= 2477:
            writer.write('%d\t%s\t%d\n' % (int(array[0]), array[1], int(array[2])))
    writer.close()
    print("KG filtered")

# Creates two dictionaries. One dictionary maps item index to entity id, and the other maps entity id to index.
def read_item_index_to_entity_id_file():
    file = '../data/item_index2entity_id.txt'
    print("reading item index to entity id file...")
    i = 0
    for line in open(file, encoding='utf-8').readlines():
        item_index = line.strip().split('\t')[0]
        satori_id = line.strip().split('\t')[1]
        item_index_old2new[item_index] = i
        entity_id2index[satori_id] = i
        i += 1
    print("Done reading item index to entity id file")

# Converts the item indices to entity indices using the dictionaries created in the previous function,
# and creates a new file 'ratings_final.txt'. Each line of this file represents a user-item interaction and contains three fields:
# user index, item index, and a binary value indicating whether the user has watched (rated) the item or not.
def convert_rating():
    file = '../data/ratings.csv'
    print('reading rating file...')
    item_set = set(item_index_old2new.values())
    user_pos_ratings = dict()
    user_neg_ratings = dict()
    for line in open(file, encoding='utf-8').readlines()[1:]:
        array = line.strip().split(',')
        item_index_old = array[1]
        if item_index_old not in item_index_old2new:
            continue
        item_index = item_index_old2new[item_index_old]
        user_index_old = int(array[0])
        rating = float(array[2])
        if rating >= 4:
            if user_index_old not in user_pos_ratings:
                user_pos_ratings[user_index_old] = set()
            user_pos_ratings[user_index_old].add(item_index)
        else:
            if user_index_old not in user_neg_ratings:
                user_neg_ratings[user_index_old] = set()
            user_neg_ratings[user_index_old].add(item_index)
    print("Done reading rating file")
    print('converting rating file ...')
    writer = open('../data/ratings_final.txt', 'w', encoding='utf-8')
    user_cnt = 0
    user_index_old2new = dict()
    for user_index_old, pos_item_set in user_pos_ratings.items():
        if user_index_old not in user_index_old2new:
            user_index_old2new[user_index_old] = user_cnt
            user_cnt += 1
        user_index = user_index_old2new[user_index_old]

        for item in pos_item_set:
            writer.write('%d\t%d\t1\n' % (user_index, item))
        unwatched_set = item_set - pos_item_set
        if user_index_old in user_neg_ratings:
            unwatched_set -= user_neg_ratings[user_index_old]
        for item in np.random.choice(list(unwatched_set), size=len(pos_item_set), replace=False):
            writer.write('%d\t%d\t0\n' % (user_index, item))
    writer.close()
    print('number of users: %d' % user_cnt)
    print('number of items: %d' % len(item_set))

def convert_rating_1M():
    file = '../data/ratings_1M.csv'
    print('reading rating file...')
    item_set = set(item_index_old2new.values())
    user_pos_ratings = dict()
    user_neg_ratings = dict()
    for line in open(file, encoding='utf-8').readlines():
        array = line.strip().split(',')
        item_index_old = array[1]
        if item_index_old not in item_index_old2new:
            continue
        item_index = item_index_old2new[item_index_old]
        user_index_old = int(array[0])
        rating = float(array[2])
        if rating >= 4:
            if user_index_old not in user_pos_ratings:
                user_pos_ratings[user_index_old] = set()
            user_pos_ratings[user_index_old].add(item_index)
        else:
            if user_index_old not in user_neg_ratings:
                user_neg_ratings[user_index_old] = set()
            user_neg_ratings[user_index_old].add(item_index)
    print("Done reading rating file")
    print('converting rating file ...')
    writer = open('../data/ratings_final.txt', 'w', encoding='utf-8')
    user_cnt = 0
    user_index_old2new = dict()
    for user_index_old, pos_item_set in user_pos_ratings.items():
        if user_index_old not in user_index_old2new:
            user_index_old2new[user_index_old] = user_cnt
            user_cnt += 1
        user_index = user_index_old2new[user_index_old]

        for item in pos_item_set:
            writer.write('%d\t%d\t1\n' % (user_index, item))
        unwatched_set = item_set - pos_item_set
        if user_index_old in user_neg_ratings:
            unwatched_set -= user_neg_ratings[user_index_old]
        for item in np.random.choice(list(unwatched_set), size=len(pos_item_set), replace=False):
            writer.write('%d\t%d\t0\n' % (user_index, item))
    writer.close()
    print('number of users: %d' % user_cnt)
    print('number of items: %d' % len(item_set))

# Converts the entity and relation ids to indices, and creates a new file 'kg_final.txt'.
# Each line of this file represents a triple in the knowledge graph and contains three fields:
# head entity index, relation index, and tail entity index.
def convert_kg():
    print('converting kg file ...')
    entity_cnt = len(entity_id2index)
    relation_cnt = 0
    writer = open('../data/kg_final.txt', 'w', encoding='utf-8')
    for line in open('../data/kg.txt', encoding='utf-8'):
        array = line.strip().split('\t')
        head_old = array[0]
        relation_old = array[1]
        tail_old = array[2]
        if head_old not in entity_id2index:
            entity_id2index[head_old] = entity_cnt
            entity_cnt += 1
        head = entity_id2index[head_old]
        if tail_old not in entity_id2index:
            entity_id2index[tail_old] = entity_cnt
            entity_cnt += 1
        tail = entity_id2index[tail_old]
        if relation_old not in relation_id2index:
            relation_id2index[relation_old] = relation_cnt
            relation_cnt += 1
        relation = relation_id2index[relation_old]
        writer.write('%d\t%d\t%d\n' % (head, relation, tail))
    writer.close()
    print('number of entities (containing items): %d' % entity_cnt)
    print('number of relations: %d' % relation_cnt)


def convert_kg_1M():
    print('converting kg file ...')
    entity_cnt = len(entity_id2index)
    relation_cnt = 0
    writer = open('../data/kg_final.txt', 'w', encoding='utf-8')
    for line in open('../data/item_kg_filtered.txt', encoding='utf-8'):
        array = line.strip().split('\t')
        head_old = array[0]
        relation_old = array[1]
        tail_old = array[2]
        if head_old not in entity_id2index:
            entity_id2index[head_old] = entity_cnt
            entity_cnt += 1
        head = entity_id2index[head_old]
        if tail_old not in entity_id2index:
            entity_id2index[tail_old] = entity_cnt
            entity_cnt += 1
        tail = entity_id2index[tail_old]
        if relation_old not in relation_id2index:
            relation_id2index[relation_old] = relation_cnt
            relation_cnt += 1
        relation = relation_id2index[relation_old]
        writer.write('%d\t%d\t%d\n' % (head, relation, tail))
    writer.close()
    print('number of entities (containing items): %d' % entity_cnt)
    print('number of relations: %d' % relation_cnt)

if __name__ == '__main__':
    np.random.seed(555)

    entity_id2index = dict()
    item_index_old2new = dict()
    relation_id2index = dict()

    # used for movieLens 20M
    read_item_index_to_entity_id_file()
    convert_rating()
    convert_kg()

    # used for MovieLens 1M
    # filterKG()
    # convert_rating_1M()
    #convert_kg_1M()

    print("Done")