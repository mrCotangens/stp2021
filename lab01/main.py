import argparse
from glob import glob
import random

class Crawler:
    def __init__(self, input_directory):
        self.input_directory = input_directory

    def get_all_songs_list(self):
        all_songs_list = []
        for file in glob(f'{self.input_directory}/song**'):
            with open(file, encoding='utf-8') as input_file:
                all_songs_list.extend(input_file.readlines())
        return all_songs_list


class Generator:
    def __init__(self, all_songs_list):
        self.all_songs_list = all_songs_list

    def generate_random_row(self):
        random_row = randint(0, len(self.all_songs_list) - 1)
        return self.all_songs_list[random_row]

    def generate_couplet(self):
        couplets_rows = int(args['rows']) - 3 * int(args['chorus'])

        couplet = []
        for row in range(couplets_rows // 3 + couplets_rows % 3):
            couplet.append(self.generate_random_row())
        yield couplet

        couplet = []
        for row in range(couplets_rows // 3):
            couplet.append(self.generate_random_row())
        yield couplet

        couplet = []
        for row in range(couplets_rows // 3):
            couplet.append(self.generate_random_row())
        yield couplet

    def generate_chorus(self):
        chorus = []
        chorus_len = int(args['chorus'])
        for row in range(chorus_len):
            chorus.append(self.generate_random_row())
        return chorus

    def generate_new_song(self):
        new_song_list = []
        couplets_generator = self.generate_couplet()
        chorus = self.generate_chorus()
        for _ in range(3):
            new_song_list.extend(next(couplets_generator))
            new_song_list.extend(['\n\n'])
            new_song_list.extend(chorus)
            new_song_list.extend(['\n\n'])
        return new_song_list


class Saver:
    def __init__(self, output_directory, new_song_list):
        self.output_directory = output_directory
        self.new_song_list = new_song_list

    def save_new_song(self):
        with open('new_song.txt', 'w+', encoding='utf-8') as output_file:
            output_file.writelines(self.new_song_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', required=False)
    parser.add_argument('-r', '--rows', required=False)
    parser.add_argument('-c', '--chorus', required=False)
    args = vars(parser.parse_args())
    # args = {'directory': r'C:\stp\stp2021', 'rows': '30', 'chorus': '5'}

    if str(args['rows']) < str(args['chorus']) * 3:
        print('Your song is smaller than 3 choruses')
        exit()

    crawler = Crawler(input_directory=args['directory'])
    generator = Generator(all_songs_list=crawler.get_all_songs_list())
    saver = Saver(output_directory=args['directory'], new_song_list=generator.generate_new_song())

    saver.save_new_song()