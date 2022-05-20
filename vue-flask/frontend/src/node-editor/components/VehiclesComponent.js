import Rete from "rete";
import * as Socket from "../sockets";

import { NumControl } from '@/node-editor/controls/NumControl/NumControl'
import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";

export class VehiclesComponent extends Rete.Component {
    constructor(){
        super("Vehicles");
    }

    builder(node) {
        var out1 = new Rete.Output('num', "Out", Socket.number);
        return node

          .addControl(new NumControl(this.editor, 'num1', false, 'Number of vehicles'))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }

    toJsonLogic(node) {
        const type = node.data.type;
        const number = node.data.num1;

        return {
            "vehicle": [ type, number ]
        }  
    }
}