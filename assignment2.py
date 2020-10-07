import yaml

with open("test2.yaml", 'r') as stream:
    try:
        contents = yaml.safe_load(stream)
        print("\n")
        for step in contents['Steps']:
             print(step['type'])
        #print(contents)
        print("\n")
    except yaml.YAMLError as exc:
        print(exc)