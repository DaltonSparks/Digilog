import React, {useEffect, useState} from 'react';
import {
  SafeAreaView,
  StyleSheet,
  View,
  FlatList,
  Image,
  TouchableOpacity,
  Button,
  Text,
} from 'react-native';



 

const CalendarView = ({navigation}) => {


  const handleUp = (value) =>{
		setIterator(value + 1)
    setMonth(months[iterator %12])
	}
  const handleDown = (value) =>{
		setIterator(value - 1)
    setMonth(months[iterator %12])
	}

  const[month,setMonth] = useState("April")


  const months = ["March","April","May","June","July","August","September","October","November","December","January","February"]
  const [iterator,setIterator] = useState(100)
  //currentMonth = months[a%12]
  //Image function that sets value for image
  

  const link = 'http://30d4-2600-1700-775-8630-d88f-82dd-84bf-821d.ngrok.io/'
  const [image, setImage] = useState(null);

  const [dataSource, setDataSource] = useState([]);

  const setLink = (index) => {
    
    return link+month+"/" + index
  }

  useEffect(() => {
    let items = Array.apply(null, Array(35)).map((v, i) => {
      return {
        id: i,
        //added the + '?' + new Date to update info because
        //without it, every time the DB would update, it would load old images
        src: setLink(i+1) + '?' + new Date(),
        //src: link + "/" + currentMonth + "/" + i
      };
    });
    setDataSource(items);
  }, [month]);

  //I tried to pass an id to this function with the touchableopacity but could not figure it out
  //We need to know what tile to display when one is pressed my idea was to pass an id of the image
  //x is the id of the tile being pressed
  DISPLAY = (x) =>
  {
    //alert("Image Clicked");
    //console.log("index", x.id);
    
    //Set the image and pass in the src/the URI of the image that has been clicked on
    setImage(x.src);
  }


  return (
    <SafeAreaView style={styles.container}>
      <View style = {{flexDirection:'row',justifyContent:'space-evenly',}}>
        <Button title = "<-" onPress={()=>handleDown(iterator)}></Button>
        <Text style={styles.smallTitle}>{month}</Text>
        <Button title = "->" onPress={()=>handleUp(iterator)}></Button>
      </View>

      <FlatList
        //horizontal = {true}// does not work with num of columns may be a way to let it rotate or a way to force it into a landscape mode
        data={dataSource}
        renderItem={({item}) => (
          <View
            style={{
              flex: 1,
              flexDirection: 'column',
              margin: 1
            }}>
            <TouchableOpacity style={styles.FacebookStyle} activeOpacity={0.5} onPress={() => setImage(item.src)}>
              {/*this.DISPLAY(item)}>*/}
            <Image
              style={styles.imageThumbnail}
              source={{uri: item.src}}
              key={new Date().getTime()}
            />
            </TouchableOpacity>
          </View>
        )}
        //Setting the number of column
        numColumns={7}
        numRows={1}
        keyExtractor={(item, index) => index}
      />
      {
      /*if Image has not been clicked on, then display nothing. Otherwise, display the image that has been clicked on*/
      }
      <TouchableOpacity style={styles.FacebookStyle} activeOpacity={0.5} onPress={() => {navigation.navigate("Merge")}}>
      {image && <Image source ={{uri:image}} style = {styles.ClickedImg}/>}
      </TouchableOpacity>
      
    </SafeAreaView>
  );
};
export default CalendarView;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    backgroundColor: 'white',
  },
  imageThumbnail: {
    justifyContent: 'center',
    alignItems: 'center',
    height: 60,
  },
  ClickedImg: {
    width: 415,
    height: 415,
    alignItems: "center",
    justifyContent: 'center',
  },
  smallTitle:{
		fontSize:20,
		textAlign:'center',
		fontWeight: "bold",
		color: '#0080c0',
		alignItems:'center',
		justifyContent:'center',
	},
});