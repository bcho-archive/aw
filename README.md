# aw

aw!

aw is a Random Dataset Generator (for my data mining learning).

Give descriptions and random generators, generate dataset.

## descriptions & generate dataset
    
    >>> from aw.builder import Desc, Dataset
    >>> from my_random_generator import * # random generator list
    >>> from my_dataset import * # dataset
    >>> movies_desc = [Desc(name='name', random_generator=movies_rg,
                     dataset=movies_set, unique=True), # movie's name cannot be same
                       Desc('rating', rating_rg)]
    >>> ds_desc = [Desc(name='name', random_generator=name_rg,
                        dataset=name_set, unique=True),
                   Desc('movies', count_rg,
                        children=movies_descs), # is a sub dataset
                   Desc('age', age_rg),
                   Desc('sexual', s_rg)]
    >>> dataset = Dataset.fromdescs(ds_desc)

## generated dataset

    >>> dataset.show()
    count: 3
    +-----------+-----------+-------+-----------+
    |   name    |   movies  |   age |   sexual  |
    +-----------+-----------+-------+-----------+
    |   Alex    |   [2]     |   19  |   male    |
    +-----------+-----------+-------+-----------+
    |   Bob     |   [7]     |   18  |   male    |
    +-----------+-----------+-------+-----------+
    |   Candy   |   [8]     |   25  |   female  |
    +-----------+-----------+-------+-----------+

    >>> len(dataset)
    3

    >>> datset.count
    3

    >>> dataset[0]
    +-----------+-----------+-------+-----------+
    |   name    |   movies  |   age |   sexual  |
    +-----------+-----------+-------+-----------+
    |   Alex    |   [15]    |   19  |   Male    |
    +-----------+-----------+-------+-----------+

    >>> '%s is a %d year's old %s.' % (dataset[0]['name'], dataset[0]['age'],\
    dataset[0].['sexual'])
    'Alex is a 18 year's old male.'

    >>> dataset[0]['movies'].show()
    count: 2
    +-------------------+-----------+
    |   name            |   rating  |
    +-------------------+-----------+
    |   Batman Beings   |   5.0     |
    +-------------------+-----------+
    |   Up in the air   |   4.0     |
    +-------------------+-----------+

    >>> dataset[0]['movies']
    +-------------------+-----------+
    |   name            |   rating  |
    +-------------------+-----------+
    |   Batman Beings   |   5.0     |
    +-------------------+-----------+
    |   Up in the air   |   4.0     |
    +-------------------+-----------+

    >>> dataset[0].movies['name']
    'Batman Beings'

    +-------------------+-----------+
    |   name            |   rating  |
    +-------------------+-----------+
    |   Batman Beings   |   5.0     |
    +-------------------+-----------+

## random generator

Write your own random generator basic on your own rule.

When entering the generator, dataset(provided in each desc) and previous
generated data will hand to the generator too.

    def a_sample_random_generator(dataset=None, previous_data=None):
        random_index = do_stuff()
        if previous_data:
            random_index = modified_random_index_base_on_pre_data()
        if dataset:
            return dataset[previous_data]
        else:
            return random_index

    def another_random_generator(dataset=None, previous_data=None):
        return do_stuff()

## TODO

* csv loader (i.e. `Dataset.fromcsv(csv_path)`)

* data persistence

* dataset formating

* data mining learning
