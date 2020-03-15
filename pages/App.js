import React, {Component} from 'react';
import {Platform, StyleSheet, Text, View, Button} from 'react-native';
import {
  accelerometer,
  gyroscope,
  setUpdateIntervalForType,
  SensorTypes,
} from 'react-native-sensors';
import { Series, DataFrame } from 'pandas-js';
const { map } = require('immutable');


const Value = ({name, value}) => (
  <View style={styles.valueContainer}>
    <Text style={styles.valueName}>{name}:</Text>
    <Text style={styles.valueValue}>{new String(value).substr(0, 8)}</Text>
  </View>
);



export default class App extends Component {


  constructor(props) {
    super(props);
    this.state = {
      acceleration: 0,
      accel_x: 0,
      accel_y: 0,
      accel_z: 0,
      gyro_x: 0,
      gyro_y: 0,
      gyro_z: 0,
      collection: false,
    };
  }

  populate_dataframe() {

   var df_1 = new DataFrame({time: 1, acc_x: 1, acc_y: 1, acc_z: 1, gyro_x: 1, gyro_y: 1, gyro_z: 1 });


    this.setState(prevState => ({
      collection: !prevState.collection,
    }));
    console.log('here');

    if (this.state.collection == true) {
      const subscription = accelerometer.subscribe(
        ({x, y, z, timestamp}) => {

            const subscription2 = gyroscope.subscribe(({g_x, g_y, g_z, timestamp}) => {
             var df_2 = new DataFrame ({
               time: timestamp, accel_x: x, accel_y: y, accel_z: z});
             df_1 = df_1.append(df_2);
              console.log("df1", df_1);

          });
          setTimeout(() => {
            subscription2.unsubscribe();

          }, 15000);
        });





      //const df_3 = concat([df_1, df_2], {ignore_index: true});
      setTimeout(() => {
        subscription.unsubscribe();
        //subscription2.unsubscribe();

      }, 15000);

    }
  }

  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.instructions}>Welcome to Dancing Queen!</Text>
        <Button
          title="hit that shit babey"
          onPress={() => this.populate_dataframe()}
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#ff6699',
  },
  instructions: {
    textAlign: 'center',
    color: '#ffffff',
    marginBottom: 5,
    fontSize: 30,
  },
  headline: {
    fontSize: 30,
    textAlign: 'center',
    margin: 10,
  },
  valueContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  valueValue: {
    width: 200,
    fontSize: 20,
  },
  valueName: {
    width: 50,
    fontSize: 20,
    fontWeight: 'bold',
  },
});
