import React,  { useState} from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Keyboard, ScrollView,ToastAndroid } from 'react-native';



const MergeView = ({navigation}) => {

	const [MD, setMD] = useState('');
	const[Event, setEvent] = useState('');
	const [taskItems, setTaskItems] = useState([]);

	
	var string = MD  + "	-	" + Event;

	
	

	const handleAddTask = () =>{
		Keyboard.dismiss();
		setTaskItems([...taskItems,string]);
		setEvent('');
		setMD('');
		ToastAndroid.showWithGravity("Event has been added to Merge List",ToastAndroid.SHORT,ToastAndroid.BOTTOM)

	}

	const finishTask = (index) =>{
		let taskCopy = [...taskItems];
		taskCopy.splice(index,1);
		setTaskItems(taskCopy);
		
	}


	return (
		<View style = {styles.container}>
			<ScrollView contentContainerStyle={{flexGrow:1}} keyboardShouldPersistTaps='handled'>
				<Text style ={styles.smallTitle}>Enter Task</Text>
				<View style = {styles.addView}>
					<View>
						<TextInput
						multiline
						style = {styles.inputBox}
						placeholder = 'e.g. March 06'
						value = {MD}
						onChangeText={(value) => setMD(value)}
						/><TextInput
						multiline
						style = {styles.inputBox}
						placeholder = 'e.g. Study for exam'
						value = {Event}
						onChangeText={(val) => setEvent(val)}
						/>
					</View>
					
					<TouchableOpacity onPress={()=> handleAddTask()} style= {styles.addButton}>
						<Text>+</Text>
					</TouchableOpacity>
				</View>
				<Text style = {styles.smallTitle}>Events to Append:</Text>
				
				{
					taskItems.map((item, index) => {
						return(
							<View key = {index} style = {styles.item}>
								<View style = {styles.itemLeft}>
									<TouchableOpacity style = {styles.box} onPress={()=>finishTask(index)}></TouchableOpacity>
									<Text style = {styles.itemText}>{item}</Text>
								</View>
							</View>
						)
					})
				}
			
			</ScrollView>

		</View>
		
	);
};

export default MergeView;


const styles = StyleSheet.create({
	container: {
		flex: 1,
		backgroundColor: '#b0e0fd',
		alignItems:'center',
		
	},

	//section titles-Enter Month Date and Enter New Event
	smallTitle:{
		fontSize:20,
		textAlign:'center',
		fontWeight: "bold",
		color: '#0080c0',
		alignItems:'center',
		justifyContent:'center',
	},

	//placeholder boxes for input text
	inputBox:{
		alignItems:'center',
		paddingVertical:5,
		paddingHorizontal:5,
		width:250,
		flexDirection: 'row',
		justifyContent:'space-between',
		borderRadius:60,
		backgroundColor: '#ffffff',
		borderWidth:2,
		borderColor:'#022299',
	},
	// + Button
	addButton:{
		width:60,
		height:60,
		backgroundColor:'#ffffff',
		borderRadius:60,
		borderWidth:2,
		borderColor:'#022299',
		justifyContent:'center',
		alignItems:'center',
	},
	addView:
	{
		flexDirection: 'row',
		alignItems:'center',
	},
	itemLeft:{
        flexDirection: 'row',
        alignItems: 'flex-start',
        flexWrap: 'wrap',
    },
    box:{
        width: 30,
        height: 30,
        backgroundColor: '#ff00aa',
        opacity: .4,
        borderRadius: 5,
        marginRight: 15,
        
    },
    itemText:{
        maxWidth:'80%',
    },
	item:{
        backgroundColor: '#fff',
        padding:10,
        borderRadius: 10,
        flexDirection: 'row',
        alignItems:'flex-start',
        justifyContent: 'space-around',
        marginBottom: 15,
       justifyContent:'flex-start',

        
    },
	
});