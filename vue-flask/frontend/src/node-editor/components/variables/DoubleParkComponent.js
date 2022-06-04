import Rete from "rete";
import * as Socket from "../../sockets";

import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";
import Node from "../../../../node_modules/rete-vue-render-plugin/src/variables/Node.vue";

export class DoubleParkComponent extends Rete.Component {
    constructor(){
        super("Double-Park");
        this.data.component = Node;
    }

    builder(node) {

        var out1 = new Rete.Output('num', "Out", Socket.number);
        return node

            .addControl(new SelectControl(this.editor, 'type1', [
                { text: 'Sensor 1 - Route 1', value: 'T1-1 ' },
                { text: 'Sensor 1 - Route 2', value: 'T1-1' },
            ], "Zone"))
            .addControl(new SelectControl(this.editor, 'type', [
                { text: 'All', value: 'ALL' },
                { text: 'Car', value: 'CAR' },
                { text: 'Truck', value: 'TRUCK' },
                { text: 'Bike', value: 'BIKE' }
              ], "Vehicle Type"))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }

    toJsonLogic(node) {
        const zone = node.data.type1;
        const vehicleType = node.data.type1;

        return {
            "doublePark": [ zone, vehicleType ] 
        }  
    }
}