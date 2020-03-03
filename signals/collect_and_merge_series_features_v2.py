import pandas as pd


class CollectAndMergeSeriesFeatures:

	def __init__(self, *args, **kwargs):
		for arg in args:
			try:
				iterator = iter(arg)
			except TypeError: # not an iterable
				print(f"The input {arg} is not an iterable")
			# not iterable
			else: # iterable
				for key in arg:
					setattr(self, key, arg[key])
		for key in kwargs:
			setattr(self, key, kwargs[key])
		self.features_names_list = [kwarg for kwarg in kwargs]
		self.n_features = len(self.features_names_list)
		self.features_dict = self.get_features_dict()
		# self.features_df = self.get_features_df()

	def __str__(self):
		meta_info = "The features contained within this CollectAndMergeSeriesFeatures obj instance are: {0}".format(self.features_names_list)
		return meta_info

	def get_features_dict(self):
		features_dict = {}
		for f in self.features_names_list:
			feature = self.__dict__.get(f, None)
			features_dict[f] = feature
		return features_dict

	def get_features_df(self):
		df = pd.concat(self.features_dict, axis=1)
		df = df.dropna()
		return df


if __name__ == "__main__":
	res = CollectAndMergeSeriesFeatures(4, x=[1,2,3], y=[4,5,6])
	
