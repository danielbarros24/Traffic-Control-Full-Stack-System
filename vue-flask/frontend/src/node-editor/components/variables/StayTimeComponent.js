import Rete from "rete";
import * as Socket from "../../sockets";

import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";
import Node from "../../../../node_modules/rete-vue-render-plugin/src/variables/Node.vue";

export class StayTimeComponent extends Rete.Component {
    constructor(){
        super("Stay Time");
        this.data.component = Node;
    }

    builder(node) {
        var out = new Rete.Output('num', "Out", Socket.number);

        return node
            .addControl(new SelectControl(this.editor, 'type', [
                { text: 'All', value: 'ALL' },
                { text: 'Car', value: 'CAR' },
                { text: 'Truck', value: 'TRUCK' },
                { text: 'Bike', value: 'BIKE' }
            ], "Vehicle Type"))
            .addControl(new SelectControl(this.editor, 'type1', [
                { text: 'Sensor 1', value: 'T1' },
                { text: 'Sensor 1', value: 'T1' }
            ], "Zone"))
            .addOutput(out);
    }

    worker(node, outputs) {
        outputs['num'] = node.data.num;
    }

    toJsonLogic(node) {
        const vehicleType = node.data.type;
        const zone = node.data.type1;

        return {
            "stayTime": [ zone, vehicleType ]
        }  
    }
}