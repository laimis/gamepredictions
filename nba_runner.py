import nba.importer as importer

def generate_features(years, train_or_test):

	output_file = f"output\\nba\\{train_or_test}\\train.csv"
	
	with open(output_file, "a", newline='') as output_f:
		output_f.write(importer.get_feature_headers())
		
		for year in years:
			input_file = f"input\\nba\\{year}.csv"
			importer.transform_csv(input_file, output_f, year)

years_train = [2015, 2016]
years_test = [2017]

generate_features(years_train, "train")
generate_features(years_test, "test")

		