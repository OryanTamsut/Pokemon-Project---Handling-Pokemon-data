from queries import heaviest_pokemon, find_roster, find_owners, finds_most_owned, find_by_type

if __name__ == '__main__':
    print(heaviest_pokemon())
    print(find_by_type("fire"))
    print(find_owners("gengar"))
    print(find_roster("Loga"))
    print(finds_most_owned())
