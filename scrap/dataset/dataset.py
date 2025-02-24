import datasets
import csv
import os
import random

class PokemonEvolution(datasets.GeneratorBasedBuilder):
    """Pokemon Evolution dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description="Pokemon Evolution dataset",
            features=datasets.Features(
                {
                    "origin" : datasets.Image(),
                    "evolution" : datasets.Image(),
                }
            ),
            supervised_keys=("origin", "evolution"),
        )

    def _split_generators(self, dl_manager):
        images_dir = "/workspaces/pokemon-infinite-evolution/scrap/dataset/images"
        metadata_path = (
            "/workspaces/pokemon-infinite-evolution/scrap/dataset/images/metadata.csv"
        )
        images = {path for path in dl_manager.iter_files(images_dir) if path.endswith('.png')}
        # for img in dl_manager.iter_files(images_dir):
        # print(img)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "images": images,
                    "metadata_path": metadata_path,
                },
            )
        ]
    def _generate_examples(self, images, metadata_path):
        base_dir = "/workspaces/pokemon-infinite-evolution/scrap/dataset/"
        with open(metadata_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                origin = row['origin']
                evolution = row['evolution']
                print(origin, evolution)
                yield random.randint(0,10000000), {
                    "origin": base_dir + origin,
                    "evolution": base_dir + evolution,
                }
