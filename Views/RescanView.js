import React, { useState, useEffect } from 'react';
import { View, Text, Button, StyleSheet, Image } from 'react-native';

const RescanView = ({taskList}) =>{

	const [date, setDate] = useState(new Date())
  	const [open, setOpen] = useState(false)

	
		
	  return(
		  <View>
			{/*
					taskList.map((item, index) => {
						return(
							<View key = {index} style = {styles.item}>
								<View style = {styles.itemLeft}>
									<TouchableOpacity style = {styles.box} onPress={()=>finishTask(index)}></TouchableOpacity>
									<Text style = {styles.itemText}>{item}</Text>
								</View>
							</View>
						)
					})
				*/
				}
		  </View>
	  )
	
	  }
export default RescanView;
	 



const styles = StyleSheet.create({
	container: {
		flex: 1,
		alignItems: 'center',
		justifyContent: 'center',
		backgroundColor: '#FFFFFF'
	},

	preview: {
		flex:1,
		alignItems: 'center',
		justifyContent:'flex-end',
	},
	imageThumbnail: {
		justifyContent: 'center',
		alignItems: 'center',
		height: 60,
	  },
});