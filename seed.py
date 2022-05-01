from datetime import datetime, timedelta, timezone, tzinfo
from pprint import pprint
from faker import Faker
from config import db
from model import *
import sys
import random
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# generate fake info
fake = Faker()

# static types in the system
USER_TYPES = [
    UserType('Normal User', False),
    UserType('Gas Station Manager', False),
    UserType('System User', True)
]


POST_TYPES = [
    PostType("Comment", True),
    PostType("Rating", False),
    PostType("Review", True),
    PostType("Promotion", False),
    PostType("Gas Price Suggestion", True),
    PostType("Amenity Tag", True)
]


GAS_TYPES = [
    GasType('Diesel'),
    GasType('87'),
    GasType('90')
]


AMENITY_TYPES = [
    AmenityType('Air pump'),
    AmenityType('Bathroom'),
    AmenityType('Convenience Store'),
]

if sys.argv:
    try:
        SEED_COUNT = int(sys.argv[0])
    except:
        SEED_COUNT =15
else:
    SEED_COUNT = 15
    

total = 0 # total records added to db

longest = 0 # longest string, formatting purposes

# lists needed for foreign keys
users:list[User] = []
posts:list[Post] = []
gasstations:list[GasStation] = []

# add the types if they dont exist in the db or fetch the type to get 
# the ID if it does exist

for i in range(len(USER_TYPES)):
    try:
        db.session.add(USER_TYPES[i])
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        USER_TYPES[i] = UserType.query.filter(UserType.user_type_name == USER_TYPES[i].user_type_name).first()
    except SQLAlchemyError as e:
        db.session.rollback()
    else:
        total += 1
    
for i in range(len(POST_TYPES)):
    try:
        db.session.add(POST_TYPES[i])
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        POST_TYPES[i] = PostType.query.filter(PostType.post_type_name == POST_TYPES[i].post_type_name).first()
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
        GAS_TYPES[i] = GasType.query.filter(GasType.gas_type_name == GAS_TYPES[i].gas_type_name).first()
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
        AMENITY_TYPES[i] = AmenityType.query.filter(AmenityType.amenity_name == AMENITY_TYPES[i].amenity_name).first()
    except SQLAlchemyError as e:
        db.session.rollback()
    else:
        total += 1       
        
longest = max(longest, len(f'   {total} type records added'))
print(f'\N{check mark}  {total} type records added')

# adding types complete


# add users

quota = 0
while quota < SEED_COUNT:
    try:
        rx = random.randint(0,1) # get a random user type between normal or manager
        utype = USER_TYPES[rx]
        u = User(fake.unique.user_name(), fake.unique.email(),fake.first_name(), fake.last_name(),fake.password(),utype)
        users.append(u)
        db.session.add(u)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
    else:
        total += 1  
        quota += 1
        print(f'\r   {quota} users added', end='', flush=True)
    
longest = max(longest, len(f'   {quota} users added'))
print('\r\N{check mark}')

# end add users

# add gas stations

quota = 0
while quota < SEED_COUNT:
    try:
        # decide randomly if this gas station should have a manager
        if random.randint(0,1): 
            rx = random.randint(0, len(users)-1) # get a random user to be the manager
            u = users[rx]
            if u.user_type.user_type_name != 'Gas Station Manager':
                u = None # set the user to None if the user's type is not manager
        else:
            u = None
        g = GasStation(fake.company(),fake.address(),fake.latitude(),fake.longitude(),fake.image(),u)
        gasstations.append(g)
        db.session.add(g)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
    else:
        total += 1 
        quota += 1
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
    postnum = random.randint(0,SEED_COUNT) 
    while quota2 < postnum:
        try:
            # get a random user to make the post
            u = users[random.randint(0,len(users)-1)]
            
            # randomly choose a post type the user is allowed make
            # based on the user type
            if u.user_type.user_type_name == 'Normal User':
                pt = random.choice([*POST_TYPES[0:3], *POST_TYPES[4:]])
            if u.user_type.user_type_name == 'Gas Station Manager':
                pt = random.choice([*POST_TYPES[4:]])
                
            p = Post(g,pt,u)
            posts.append(p)
            db.session.add(p)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
        else:
            total += 1 
            quota += 1
            quota2 += 1
            print(f'\r   {quota} posts added', end='', flush=True)
    else:
        i +=1

print('\r\N{check mark}')
longest = max(longest, len(f'   {quota} posts added'))

# end add posts


# add post details 

quota = 0
while quota < len(posts):
    try:
        ptn =posts[quota].post_type.post_type_name # post type name
        
        # create post details based on post type
        if ptn == 'Comment':
            rev = Review(posts[quota])
            c = Comment(fake.paragraph(nb_sentences=3),rev)
            db.session.add(rev)
            db.session.add(c)
            db.session.commit()
        elif ptn == 'Rating':
            rev = Review(posts[quota])
            ra = Rating(random.randint(1,5),rev)
            db.session.add(rev)
            db.session.add(ra)
            db.session.commit()
        elif ptn == 'Review':
            rev = Review(posts[quota])
            c = Comment(fake.paragraph(nb_sentences=3),rev)
            ra = Rating(random.randint(1,5),rev)
            db.session.add(rev)
            db.session.add(c)
            db.session.add(ra)
            db.session.commit()
        elif ptn == 'Promotion':
            start_date = fake.future_datetime(tzinfo=timezone.utc)            
            end_date = start_date + timedelta(days=random.randint(1,30))
            promo = Promotion(start_date,end_date,fake.image(),fake.paragraph(nb_sentences=2),posts[quota])
            db.session.add(promo)
            db.session.commit()
        elif ptn == 'Gas Price Suggestion':
            gps = GasPriceSuggestion(posts[quota])
            # choose random gas types
            num = random.randint(0, len(GAS_TYPES)-1)
            types = random.choices(population=GAS_TYPES, k=num)
            gps_gases = [Gas(fake.pyfloat(positive=True), t, gps) for t in types]
            gps.gases = gps_gases
            db.session.add(gps)
            db.session.commit()
        elif ptn == 'Amenity Tag':
            a = AmenityTag(AMENITY_TYPES[random.randint(0, len(AMENITY_TYPES)-1)],posts[quota])
            db.session.add(a)
            db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
    else:
        total += 1 
        quota += 1
        print(f'\r   {quota} post details added', end='', flush=True)

print('\r\N{check mark}')
longest = max(longest, len(f'   {quota} post details added'))

# end add post details

print('='*longest)
print(f'\N{check mark}  {total} records added')
print('='*longest)
