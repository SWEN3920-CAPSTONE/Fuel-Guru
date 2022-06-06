"""
Generates Fake Test data for the Fuel Guru db

usage:  python seed.py [<int>]

<int>:  Integer value. Determines the base number of records 
        to add for each table. Default value is 15
"""

import base64
import random
import sys
from datetime import timedelta, timezone

from faker import Faker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from config import db, app
from model.users import *
from model.gasstation import *
from model.posts import *

# generate fake info
fake = Faker()

# static types in the system
USER_TYPES = [
    UserType('Normal User', False, True),
    UserType('Gas Station Manager', False, False),
    UserType('System User', True, False)
]

POST_TYPES = [
    PostType("Review",False),
    PostType("Promotion", False),
    PostType("Gas Price Suggestion", True),
    PostType("Amenity Tag", True)
]

ALLOWED_POST_TYPES = [
    lambda: [POST_TYPES[0], POST_TYPES[2],
             POST_TYPES[3]],
    lambda: [POST_TYPES[1], POST_TYPES[2], POST_TYPES[3]],
    lambda: [POST_TYPES[2], POST_TYPES[3]]
]

GAS_TYPES = [
    GasType('Diesel'),
    GasType('87'),
    GasType('90'),
    GasType('ULSD')
]


AMENITY_TYPES = [
    AmenityType('Air pump'),
    AmenityType('Bathroom'),
    AmenityType('Convenience Store'),
]

# get commandline args
if sys.argv:
    try:
        SEED_COUNT = int(sys.argv[1])
    except IndexError:
        SEED_COUNT = 15
    except ValueError as e:
        print(f'Invalid int for seed count arg: <{sys.argv[1]}>')
        SEED_COUNT = 15
    except:
        SEED_COUNT = 15
else:
    SEED_COUNT = 15


total = 0  # total records added to db

longest = 0  # longest string, formatting purposes

# lists needed for foreign keys
users: list[User] = []
posts: list[Post] = []
gasstations: list[GasStation] = []

db.session.autoflush = True
# add the types if they dont exist in the db or fetch the type to get
# the ID if it does exist

for i in range(len(POST_TYPES)):
    try:
        db.session.add(POST_TYPES[i])
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        POST_TYPES[i] = PostType.query.filter(
            PostType.post_type_name == POST_TYPES[i].post_type_name).first()
    except SQLAlchemyError as e:
        db.session.rollback()
    else:
        total += 1


for i in range(len(USER_TYPES)):
    try:
        USER_TYPES[i].allowed_post_types = ALLOWED_POST_TYPES[i]()

        db.session.add(USER_TYPES[i])
        db.session.flush()
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        USER_TYPES[i] = UserType.query.filter(
            UserType.user_type_name == USER_TYPES[i].user_type_name).first()
    except SQLAlchemyError as e:
        db.session.rollback()
    else:
        total += 1


for i in range(len(GAS_TYPES)):
    try:
        db.session.add(GAS_TYPES[i])
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        GAS_TYPES[i] = GasType.query.filter(
            GasType.gas_type_name == GAS_TYPES[i].gas_type_name).first()
    except SQLAlchemyError as e:
        db.session.rollback()
    else:
        total += 1


for i in range(len(AMENITY_TYPES)):
    try:
        db.session.add(AMENITY_TYPES[i])
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        AMENITY_TYPES[i] = AmenityType.query.filter(
            AmenityType.amenity_name == AMENITY_TYPES[i].amenity_name).first()
    except SQLAlchemyError as e:
        db.session.rollback()
    else:
        total += 1


for i in range(len(ALLOWED_POST_TYPES)):
    try:
        USER_TYPES[i].allowed_post_types = ALLOWED_POST_TYPES[i]()
        db.session.flush()
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()

if app.config.get('IS_DEV'):

    longest = max(longest, len(f'   {total} type records added'))
    print(f'\N{check mark}  {total} type records added')

    # adding types complete

    # add users

    quota = 0
    while quota < SEED_COUNT:
        try:
            # make sure at least one user of each type exists in the database
            if quota == 0:
                rx = 0
            elif quota == 1:
                rx = 1
            elif quota == 2:
                rx = 2
            else:
                # get a random user type between normal or manager
                rx = random.randint(0, 1)

            utype = USER_TYPES[rx]

            username = fake.unique.user_name()
            password = fake.password(length=12)

            u = User(username, fake.unique.email(),
                    fake.first_name(), fake.last_name(), password, utype)
            users.append(u)

            db.session.add(u)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
        else:
            total += 1
            quota += 1
            print(f'\r   {quota} users added', end='', flush=True)
    else:
        print(f'\r   {quota} users added', end='', flush=True)

    longest = max(longest, len(f'   {quota} users added'))
    print('\r\N{check mark}')

    # end add users


    # add gas stations

    quota = 0
    while quota < SEED_COUNT:
        try:
            # decide randomly if this gas station should have a manager
            if random.randint(0, 1):
                # get a random user to be the manager
                rx = random.randint(0, len(users)-1)
                u = users[rx]
                if u.user_type.user_type_name != 'Gas Station Manager':
                    u = None  # set the user to None if the user's type is not manager
            else:
                u = None
            g = GasStation(fake.company(), fake.address(),
                        fake.latitude(), fake.longitude(), base64.b64encode(fake.image()).decode('utf-8'), u)
            gasstations.append(g)
            db.session.add(g)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
        else:
            total += 1
            quota += 1
            print(f'\r   {quota} gas stations added', end='', flush=True)
    else:
        print(f'\r   {quota} gas stations added', end='', flush=True)


    print('\r\N{check mark}')
    longest = max(longest, len(f'   {quota} gas stations added'))

    # end add gas stations


    # add posts

    quota = 0
    while i < SEED_COUNT:
        # get the gas station to add posts to
        g = gasstations[i]
        quota2 = 0
        # choose a random amount of posts to add to each gas station
        postnum = random.randint(0, SEED_COUNT)
        while quota2 < postnum:
            try:
                # get a random user to make the post
                u = users[random.randint(0, len(users)-1)]

                pt = None
                # randomly choose a post type the user is allowed make
                # based on the user type
                if u.user_type.user_type_name == 'Normal User':
                    pt = random.choice([*POST_TYPES[0:3], *POST_TYPES[4:]])
                if u.user_type.user_type_name == 'Gas Station Manager':
                    if g.manager == u:
                        pt = random.choice([*POST_TYPES[3:]])
                    else:
                        continue

                p = Post(g, pt, u)
                db.session.add(p)
                db.session.commit()
                posts.append(p)
            except SQLAlchemyError as e:
                db.session.rollback()
            else:
                total += 1
                quota += 1
                quota2 += 1
                print(f'\r   {quota} posts added', end='', flush=True)
        else:
            i += 1
    else:
        print(f'\r   {quota} posts added', end='', flush=True)


    print('\r\N{check mark}')
    longest = max(longest, len(f'   {quota} posts added'))

    # end add posts


    # add post details

    quota = 0
    while quota < len(posts):
        try:
            ptn = posts[quota].post_type.post_type_name  # post type name

            # create post details based on post type
            if ptn == 'Review':
                rev = Review(posts[quota],fake.paragraph(nb_sentences=3),random.randint(1, 5))
                db.session.add(rev)
                db.session.commit()
            elif ptn == 'Promotion':
                start_date = fake.future_datetime(tzinfo=timezone.utc)
                end_date = start_date + timedelta(days=random.randint(1, 30))
                promo = Promotion(start_date, end_date, base64.b64encode(fake.image()).decode('utf-8'), fake.paragraph(nb_sentences=2), posts[quota])
                db.session.add(promo)
                db.session.commit()
            elif ptn == 'Gas Price Suggestion':
                gps = GasPriceSuggestion(posts[quota])
                # choose random gas types
                num = random.randint(1, len(GAS_TYPES))
                types = random.choices(population=GAS_TYPES, k=num)
                gps_gases = [Gas(fake.pyfloat(positive=True), t, gps)
                            for t in types]
                gps.gases = gps_gases
                db.session.add(gps)
                db.session.commit()
            elif ptn == 'Amenity Tag':
                a = AmenityTag(AMENITY_TYPES[random.randint(
                    0, len(AMENITY_TYPES)-1)], posts[quota])
                db.session.add(a)
                db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
        else:
            total += 1
            quota += 1
            print(f'\r   {quota} post details added', end='', flush=True)
    else:
        print(f'\r   {quota} post details added', end='', flush=True)

    print('\r\N{check mark}')
    longest = max(longest, len(f'   {quota} post details added'))

    # end add post details

    # add upvotes
    quota = 0
    i = 0
    while i < len(posts):
        fails = 0
        # get the post to add upvotes to
        p = posts[i]
        quota2 = 0
        # choose a random amount of upvotes to add to each post
        usernum = random.randint(0, SEED_COUNT-1)
        while quota2 < usernum:
            try:
                # get a random user to make the upvote
                u = users[random.randint(0, len(users)-1)]

                # only normal users can upvote
                if u.user_type.user_type_name == 'Normal User':
                    # if the user is the creator or the user is already an upvoter, skip
                    if p.creator == u or u in p.upvoters:
                        raise SQLAlchemyError('This user is the creator or already upvoted')
                    if u in p.downvoters:
                        p.downvoters.remove(u)
                    p.upvoters.append(u)

                    db.session.commit()
                    fails = 0
                else:
                    raise SQLAlchemyError('This user can\'t upvote')
            except SQLAlchemyError as e:
                fails+=1
                if fails>5:
                    quota2 = usernum 
                db.session.rollback()
            else:
                total += 1
                quota += 1
                quota2 += 1
                print(f'\r   {quota} upvotes added', end='', flush=True)
        else:
            i += 1
    else:
        print(f'\r   {quota} upvotes added', end='', flush=True)

    print('\r\N{check mark}')
    longest = max(longest, len(f'   {quota} upvotes added'))

    # end add upvotes

    # add downvotes
    quota = 0
    i = 0
    while i < len(posts):
        fails = 0
        # post to add downvotes to
        p = posts[i]
        quota2 = 0
        # choose a random amount of downvotes to add to each post
        usernum = random.randint(0, SEED_COUNT-1)
        while quota2 < usernum:
            try:
                # get a random user to make the downvote
                u = users[random.randint(0, len(users)-1)]

                # only normal users can downvote
                if u.user_type.user_type_name == 'Normal User':
                    # if the user is the creator or the user is already a downvoter or upvoter, skip
                    if p.creator == u or u in p.downvoters or u in p.upvoters:
                        raise SQLAlchemyError('This user is the creator or already upvoted')
                    
                    p.downvoters.append(u)

                    db.session.commit()
                    fails = 0
                else:
                    raise SQLAlchemyError('This user can\'t upvote')
            except SQLAlchemyError as e:
                fails+=1
                if fails>5:
                    quota2 = usernum 
                    
                db.session.rollback()
            else:
                total += 1
                quota += 1
                quota2 += 1
                print(f'\r   {quota} downvotes added', end='', flush=True)
        else:
            i += 1
    else:
        print(f'\r   {quota} downvotes added', end='', flush=True)

    print('\r\N{check mark}')
    longest = max(longest, len(f'   {quota} downvotes added'))

    # end add downvotes

    print('='*longest)
    print(f'\N{check mark}  {total} records added')
    print('='*longest)
