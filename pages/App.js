import React, {Component} from 'react';
import {Platform, StyleSheet, Text, View, Button} from 'react-native';
import {
  accelerometer,
  gyroscope,
  setUpdateIntervalForType,
  SensorTypes,
} from 'react-native-sensors';
import { Series, DataFrame } from 'pandas-js';


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
    };

    accelerometer.subscribe(({x, y, z, timestamp}) =>
        console.log("accel" ,{ x, y, z, timestamp })
     /* this.setState(
        ((this.state.accel_x = {x}),
        (this.state.accel_y = {y}),
        (this.state.accel_z = {z})),
      ), */
    );

    gyroscope.subscribe(({x, y, z, timestamp}) =>
      /*this.setState(
        ((this.state.gyro_x = {x}),
        (this.state.gyro_y = {y}),
        (this.state.gyro_z = {z})),
      ),*/
        console.log("gyro" ,{ x, y, z, timestamp })
    );
  }

  populate_dataframe() {

    console.log("here");
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
