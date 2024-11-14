import shutil
import os

currentdir = os.curdir

import polar_fox

consumers = [
    ("CHIPS", "chips"),
    ("FIRS", "firs"),
    ("Iron_Horse", "iron-horse"),
    ("Road_Hog", "road-hog"),
    ("Unsinkable_Sam", "unsinkable-sam"),
]


def main():
    print("[DISTRIBUTING TO DOWNSTREAM CONSUMERS]")
    # this assumes that consumers are found in a consistent ../../ location, and have a consistent Project_name/repo-name structure
    consumer_root = os.path.dirname(os.path.dirname(os.path.abspath(currentdir)))
    for consumer in consumers:
        print("..." + consumer[0])
        consumer_dst_path = os.path.join(
            consumer_root, consumer[0], consumer[1], "src", "polar_fox"
        )
        if os.path.exists(consumer_dst_path):
            shutil.rmtree(consumer_dst_path)
        shutil.copytree(os.path.join(polar_fox.dist_package_path), consumer_dst_path)
    print("[DISTRIBUTING TO DOWNSTREAM CONSUMERS] - complete")
    print("Don't forget to test and commit changes for each consumer")


if __name__ == "__main__":
    main()
