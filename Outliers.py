class Outlier_detector_and_remover :
	'''
	This is a class for detecting and removal of utliers in a feature of a dataframe.

	Availaible methods for this class are as follows :

		* 'TUKEY_outlier_detector' >> Detection of outliers in a feature of a dataframe, utilising IQR.
		* 'TUKEY_outlier_remover' >> Removal of outliers in a feature of a dataframe, utilising IQR.
        * 'operate' >> To carry out the desired method between 'detection' and 'removal'

	Class parameters are as follows :
		* dataframe - name of the dataframe of the data in use.
		* feature - name of the feature in the dataframe, to detect and manage the outliers.
	'''
	
	def __init__(self, dataframe, feature, operate_type):

		self.dataframe = dataframe
		self.feature = feature
		self.operate_type = operate_type
        
	def TUKEY_outlier_detector(self):

		'''
		 Input: 
		   - pandas dataframe (self.dataframe)
		   - name of the column to analyze (self.feature)
		 Output:
		   To print out the following information about the data :
		   - interquartile range
		   - upper_inner_fence
		   - lower_inner_fence
		   - upper_outer_fence
		   - lower_outer_fence
		   - percentage of records out of inner fences
		   - percentage of records out of outer fences
		'''
		a = self.dataframe[self.feature].describe()

		q3 = a["75%"]
		q1 = a["25%"]

		iqr = q3 - q1
		print("interquartile range:", iqr)

		upper_inner_fence = q3 + 1.5 * iqr
		lower_inner_fence = q1 - 1.5 * iqr
		print("upper_inner_fence:", upper_inner_fence)
		print("lower_inner_fence:", lower_inner_fence)

		upper_outer_fence = q3 + 3 * iqr
		lower_outer_fence = q1 - 3 * iqr
		print("upper_outer_fence:", upper_outer_fence)
		print("lower_outer_fence:", lower_outer_fence)

		count_over_upper = len(self.dataframe[self.dataframe[self.feature]>upper_inner_fence])
		count_under_lower = len(self.dataframe[self.dataframe[self.feature]<lower_inner_fence])
		percentage = 100 * (count_under_lower + count_over_upper) / a["count"]
		print("percentage of records out of inner fences for "  +self.feature+ " is: %.2f"% (percentage))

		count_over_upper = len(self.dataframe[self.dataframe[self.feature]>upper_outer_fence])
		count_under_lower = len(self.dataframe[self.dataframe[self.feature]<lower_outer_fence])
		percentage = 100 * (count_under_lower + count_over_upper) / a["count"]
		print("percentage of records out of outer fences for "  +self.feature+ " is: %.2f"% (percentage))


	def TUKEY_outlier_remover(self):
		'''
		 Input: 
		   - pandas dataframe (self.dataframe)
		   - name of the column to analyze (self.feature)
		   - inner (1.5*iqr) or outer (3.0*iqr) (fence) values: "inner" or "outer"
		 Output:
			Remove outliers according to the given fence value.
		   - and return a new pandas dataframe (outliers_removed_df)
		'''

		# user input
		fence = str(input('State the fence type to remove outliers relative to it :'))

		# # making the return variable 'global', for further use of it in the project.
		global outliers_removed_df


		a = self.dataframe[self.feature].describe()

		q3 = a["75%"]
		q1 = a["25%"]

		iqr = q3 - q1
				
		upper_inner_fence = q3 + 1.5 * iqr
		lower_inner_fence = q1 - 1.5 * iqr
				
		upper_outer_fence = q3 + 3 * iqr
		lower_outer_fence = q1 - 3 * iqr
				
		count_over_upper = len(self.dataframe[self.dataframe[self.feature]>upper_inner_fence])
		count_under_lower = len(self.dataframe[self.dataframe[self.feature]<lower_inner_fence])
		percentage = 100 * (count_under_lower + count_over_upper) / a["count"]
				
		count_over_upper = len(self.dataframe[self.dataframe[self.feature]>upper_outer_fence])
		count_under_lower = len(self.dataframe[self.dataframe[self.feature]<lower_outer_fence])
		percentage = 100 * (count_under_lower + count_over_upper) / a["count"]
				
		if fence == "inner":
			outliers_removed_df = self.dataframe[self.dataframe[self.feature]<=upper_inner_fence]
			outliers_removed_df = outliers_removed_df[outliers_removed_df[self.feature]>=lower_inner_fence]
		elif fence == "outer":
			outliers_removed_df = self.dataframe[self.dataframe[self.feature]<=upper_outer_fence]
			outliers_removed_df = outliers_removed_df[outliers_removed_df[self.feature]>=lower_outer_fence]
		else:
			raise Exception('Wrong type of fence applied.')

		print("length of input dataframe:", len(self.dataframe))
		print("length of new dataframe after outlier removal:", len(outliers_removed_df))

		return outliers_removed_df


	def operate(self):
		if self.operate_type == "detection" :
			return self.TUKEY_outlier_detector()
		elif self.operate_type == "removal" :
			return self.TUKEY_outlier_remover()
		else :
			raise Exception("The type of operation on the feature not understood.")