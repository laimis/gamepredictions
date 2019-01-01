__levels__ =  [
	(0.60, 0.70),
	(0.70, 0.80),
	(0.80, 0.90),
	(0.90, 1.10),
	(0.60, 1.10),
	(0.70, 1.10),
	(0.80, 1.10)
]

def get_money_amount_from_line(spread:float) -> Tuple[int,int]:
	if (spread >= -1):
		return (5,5)
	if (spread >= -3):
		return (3,5)
	if (spread >= -5):
		return (1,5)
	if (spread >= -8):
		return (1, 8)
	if (spread >= -10):
		return (1, 10)
	return (1,15)

def confidence_stats(model, X, y, line_data=None) -> List[ConfidenceStat]:

	def calc_confidence_stats(y, predicted, probabilities, level):
		correct_count = 0
		total_count = 0
		money = 0

		for i,_ in enumerate(predicted):
			if np.max(probabilities[i]) >= level[0] and np.max(probabilities[i]) < level[1]:
				money_amount = get_money_amount_from_line(line_data[i])
				total_count += 1
				if y[i] == predicted[i]:
					correct_count += 1
					money += money_amount[0]
				else:
					money -= money_amount[1]

		return ConfidenceStat(level, correct_count, total_count, money)

	predictions = model.predict(X)
	probabilities = model.predict_proba(X)

	stats = []
	for level in __levels__:
		stat = calc_confidence_stats(y, predictions, probabilities, level)
		stats.append(stat)

	return stats