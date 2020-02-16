import React, {Component} from 'react';
import {Platform, StyleSheet, Text, View} from 'react-native';
import {
  setUpdateIntervalForType,
  SensorTypes,
  accelerometer,
  gyroscope,
} from 'react-native-sensors';

const Value = ({name, value}) => (
  <View style={styles.valueContainer}>
    <Text style={styles.valueName}>{name}:</Text>
    <Text style={styles.valueValue}>{new String(value).substr(0, 8)}</Text>
  </View>
);

export default class App extends Component {
  constructor(props) {
    super(props);

    setUpdateIntervalForType(SensorTypes.accelerometer, 200);
    this.accelSubscription = accelerometer.subscribe(({x, y, z, timestamp}) =>
      this.setState({
        accel_x: x,
        accel_y: y,
        accel_z: z,
      }),
    );

    this.state = {
      acceleration: 0,
      accel_x: 0,
      accel_y: 0,
      accel_z: 0,
    };
  }

  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.instructions}>Welcome to Dancing Queen!</Text>
        <Text style={styles.headline}>
          Accelerometer values
        </Text>
        <Value name="x" value={this.state.x} />
        <Value name="y" value={this.state.y} />
        <Value name="z" value={this.state.z} />git
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
