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
      collection: false,
    };
  }

  populate_dataframe() {

    this.setState(prevState => ({
      collection: !prevState.collection,
    }));
    console.log('here');

    if (this.state.collection == true) {
      const subscription = accelerometer.subscribe(
        ({x, y, z, timestamp}) => {//console.log('accel', {x, y, z, timestamp})
         /* const df2 = new DataFrame({
            time: [timestamp],
            accel_x: [x],
            accel_y: [y],
            accel_z: [z],
          }, ['time', 'accel_x', 'accel_y', 'accel_z']);
          this.df_a.join(df2, ['time', 'accel_x', 'accel_y', 'accel_z'], "full");*/
        });

      const subscription2 = gyroscope.subscribe(({x, y, z, timestamp}) => {

        //console.log('gyro', {x, y, z, timestamp}),
        /*const df3 = new DataFrame({
          gyro_x: [x],
          gyro_y: [y],
          gyro_z: [z],
        }, ['gyro_x', 'gyro_y', 'gyro_z']);
        this.df_g.join(df3, ['gyro_x', 'gyro_y', 'gyro_z'], "full");*/
      });

      setTimeout(() => {
        subscription.unsubscribe();
        subscription2.unsubscribe();

       // this.df_a.join(this.df_g, ['time', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z'], "full");

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
