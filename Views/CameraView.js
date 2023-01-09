import React, {useState, useEffect} from 'react';
import {Camera} from 'expo-camera';
import {useIsFocused} from '@react-navigation/native'
import { View, Text, Button, StyleSheet, Image,ToastAndroid } from 'react-native';

const CameraView = ({navigation}) => {
        const handleUp = (value) =>{
            setIndex(value + 1)
            console.log(currentMonth)
        }
    const handleDown = (value) =>{
            setIndex(value - 1)
            console.log(currentMonth)
        }
    const[a,setIndex] = useState(1)

    months = ["March","April","May","June","July","August","September","October","November","December","January","February"]

    currentMonth = months[a%12]
  





    const focused = useIsFocused()   
    const [CameraPermission, setCameraPermission] = useState(null);
    const [camera,setCamera] = useState(null);
    const [image, setImage] = useState(null);
    const [type, setType] = useState(Camera.Constants.Type.back);



    const uploadImage = (data,currentMonth) => {
        try {
                
            const form_data = new FormData();
            //formData only accepts blobs, files, and strings
            form_data.append("pic", {uri:data.uri, type: 'image/jpeg', name:currentMonth});
            //form_data.append("currentMonth", currentMonth)
            //let response = await fetch('http://127.0.0.1:5000/upload', {
            {
                //I needed to use ngrok in order to use fetch
                //start it by going to directory and type ngrok http 5000 and paste link as shown below

            }
           
            {
                let response =  fetch('http://30d4-2600-1700-775-8630-d88f-82dd-84bf-821d.ngrok.io/upload', {
                    method: 'POST',
                    body: form_data,
                    headers:{
                        'Content-Type': 'multipart/form-data',
                    },
                });
                if (response.ok){
                    let json =  response.json();
                    return true;
                }
                else{
                    console.log();
                    return false;
                }
            }
        }
        catch (error){
            console.error(error);
            return false;
        }
    }
    useEffect(() => {
        (async () => {
            const Camerastatus = await Camera.requestCameraPermissionsAsync();
            setCameraPermission(Camerastatus.status === 'granted');
        }) ();
    }, []);


    const takePicture = async () => {
        if(camera)
        {
            const data = await camera.takePictureAsync(null)
            setImage(data.uri);
            uploadImage(data,currentMonth);
            //navigation.navigate('Calendar')
            ToastAndroid.showWithGravity("Image Taken Successfully, Please Move to Calendar View to See Updates",ToastAndroid.SHORT,ToastAndroid.BOTTOM)
        }
    }

    if(CameraPermission === null){
        return <View />;
    }
    if (CameraPermission === false){
        return  <Text>NO ACCESS TO CAMERA</Text>;
    }

    return(
        
        <View style = {{flex: 1}}>
            <View style = {{flexDirection:'row',justifyContent:'space-evenly',}}>
            <Button title = "<-" onPress={()=>handleDown(a)}></Button>
            <Text style={styles.smallTitle}>{currentMonth}</Text>
            <Button title = "->" onPress={()=>handleUp(a)}></Button>
        </View>
            {focused && <Camera style = {styles.camera} type = {type}
                ref = {ref=> setCamera(ref)}

                />
            }
            <Button
            title = "Take Picture"
            onPress = {() => takePicture()}
            />
            
            

            {
                //If take picture is pressed, the image will be displayed
                //{image && <Image source ={{uri:image}} style = {{flex: 1}}/>}
            }
            
        </View>
    )
};

export default CameraView;

const styles = StyleSheet.create({
    camera: {
        flex: 1,
        flexDirection: 'row'
    },
    fixedRatio:{
        flex: 1,
        aspectRatio: 2,
    },

})