import { Socket } from "rete";

const number = new Socket('Number');
const boolean = new Socket('Boolean');
const constant = new Socket('Constant')
const vehicle = new Socket('Vehicle');

constant.combineWith(number);

//const road = new Socket('Road');
//road.combineWith(all);

export { 
    number,
    boolean,
    constant,
    vehicle
};

