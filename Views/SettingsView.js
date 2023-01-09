import React from 'react';
import { View, Text, Button, StyleSheet, Image } from 'react-native';

const SettingsView = ({navigation}) => {
	return (
		<View style = {styles.container}>
			
			<Image
				resizeMode = 'center'
				source ={require('../assets/construction.jpg')}
			/>
		</View>
	);
};

export default SettingsView;

const styles = StyleSheet.create({
	container: {
		flex: 1,
		alignItems: 'center',
		justifyContent: 'center',
		backgroundColor:'#ff8000'
	},
});