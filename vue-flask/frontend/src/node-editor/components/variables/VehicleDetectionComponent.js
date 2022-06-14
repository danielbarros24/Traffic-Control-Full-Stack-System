import Rete from "rete";
import * as Socket from "../../sockets";

import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";
import Node from "../../../../node_modules/rete-vue-render-plugin/src/variables/Node.vue";

export class VehicleDetectionComponent extends Rete.Component {
    constructor(){
        super("Vehicle Detection");
        this.data.component = Node;
    }

    async builder(node) {

        const responseZones = await fetch("http://192.168.1.216:5000/sensors");
        const sensors = await responseZones.json();

        const all = []


        for (const x in sensors) {

            const sensor = sensors[x]
            const lanes = sensor.lanes

            const n = 1

            const aux = []

            while (lanes > 0) {

                aux = [];
                aux.push(sensor.name);
                aux.push(n);

                all.push(aux);

                n ++;
                lanes --;

            }
        } 

        var out1 = new Rete.Output('num', "Out", Socket.number);

        return node
          .addControl(new SelectControl(this.editor, 'type', [
            { text: 'All', value: 'ALL' },
            { text: 'Car', value: 'CAR' },
            { text: 'Truck', value: 'TRUCK' },
            { text: 'Bicycle', value: 'BICYCLE' }
          ], "Vehicle Type"))
          .addControl(new SelectControl(this.editor, 'type1', all.map((value) => ({
            text: `${value[0]} - Lane ${value[1]}`, value: `${value[0]}-${value[1]}`,
        })), "Zone"))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.type;
    }

    toJsonLogic(node) {
        const type = node.data.type;
        const zone = node.data.type1;

        return {
            "vehicleDetection": [zone, type]
        }  
    }
}