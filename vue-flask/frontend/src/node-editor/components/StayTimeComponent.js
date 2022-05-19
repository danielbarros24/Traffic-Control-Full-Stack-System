import Rete from "rete";
import * as Socket from "../sockets";

import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";

export class StayTimeComponent extends Rete.Component {
    constructor(){
        super("Stay Time");
    }

    builder(node) {
        var out = new Rete.Output('num', "Out", Socket.number);

        return node
            .addControl(new SelectControl(this.editor, 'type', [
                { text: 'All', value: 'ALL' },
                { text: 'Car', value: 'CAR' },
                { text: 'Truck', value: 'TRUCK' },
                { text: 'Motocycle', value: 'MOTO' }
            ], "Vehicle Type"))
            .addControl(new SelectControl(this.editor, 'type1', [
                { text: 'Sensor 1 - Route 1', value: 'T1-1' },
                { text: 'Sensor 1 - Route 2', value: 'T1-2' }
            ], "Zone"))
            .addOutput(out);
    }

    worker(node, outputs) {
        outputs['num'] = node.data.num;
    }

    toJsonLogic(node) {
        const type = node.data.type;
        const zone = node.data.type1;

        return {
            "stayTime": [ type, zone ]
        }  
    }
}