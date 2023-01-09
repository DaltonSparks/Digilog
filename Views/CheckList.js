import React from 'react';
import {View, Text, StyleSheet, TouchableOpacity} from 'react-native';

const InfoDate = (props) => {
    return(
        <View style = {styles.item}>
            <View style = {styles.itemLeft}>
                <TouchableOpacity style = {styles.box}></TouchableOpacity>
                <Text style = {styles.itemText}>{props.text}</Text>
            </View>
            
        </View>
    )
}

const styles = StyleSheet.create({
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
    
})

export default InfoDate;