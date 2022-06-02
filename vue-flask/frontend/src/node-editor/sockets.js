import { Socket } from "rete";

const number = new Socket('Number');
const boolean = new Socket('Boolean');
const constant = new Socket('Constant')
const vehicle = new Socket('Vehicle');
const road = new Socket('Road');
const all = new Socket('All');

number.combineWith(all);
boolean.combineWith(all);
vehicle.combineWith(all);
road.combineWith(all);

constant.combineWith(number);

export { 
    number,
    boolean,
    constant,
    vehicle,
    road,
    all
};

