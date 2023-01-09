import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

import CalendarView from '../Views/CalendarView';
import CameraView from '../Views/CameraView';
import MergeView from '../Views/MergeView';
import RescanView from '../Views/RescanView';
import SettingsView from '../Views/SettingsView';
import { Ionicons } from '@expo/vector-icons';
import { backgroundColor } from 'react-native/Libraries/Components/View/ReactNativeStyleAttributes';

const Tab = createBottomTabNavigator();

const Tabs = () => {
	return(
		<Tab.Navigator
		screenOptions=
		{({ route }) => ({
			tabBarStyle: {backgroundColor: '#00ff'},
			tabBarIcon: ({ focused, size, color }) => {
			  let iconName;
			  if (route.name === 'Camera') {
				iconName = 'camera';
				size = focused ? 25 : 20;
				
				
			  } else if (route.name === 'Merge') {
				iconName = 'git-merge';
				size = focused ? 25 : 20;
				
			  }
			  else if (route.name === 'Calendar') {
				iconName = 'calendar';
				size = focused ? 25 : 20;
			  }
			  else if (route.name === 'Rescan') {
				iconName = 'refresh';
				size = focused ? 25 : 20;
			  }
			  else if (route.name === 'Settings') {
				iconName = 'settings';
				size = focused ? 25 : 20;
			  }
			  return (
				// Required Ionicons for expo instead of vector-icons
				<Ionicons
				  name={iconName}
				  size={size}
				  color={focused ? '#00aa' : '#aaff'}
				  
				/>
			  )
			}
		  })
		}

		  activeColor='#00ffaa'
		  inactiveColor = '#4157be'
		  barStyle={{ backgroundColor: '#0040aa' }}

		>

			<Tab.Screen name = "Rescan" component = {RescanView}/>
			<Tab.Screen name = "Merge" component = {MergeView}/>
			<Tab.Screen name = "Calendar" component = {CalendarView}/>
			<Tab.Screen name = "Camera" component = {CameraView}/>
			<Tab.Screen name = "Settings" component = {SettingsView}/>
		</Tab.Navigator>
	);
}

export default Tabs;