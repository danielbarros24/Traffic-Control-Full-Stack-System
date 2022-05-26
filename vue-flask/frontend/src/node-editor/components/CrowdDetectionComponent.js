import Rete from "rete";
import * as Socket from "../sockets";

import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";


export class CrowdDetectionComponent extends Rete.Component {
    constructor(){
        super("Crowd Detection");
    }

    builder(node) {

        var out1 = new Rete.Output('num', "Out", Socket.number);
        return node

            .addControl(new SelectControl(this.editor, 'type1', [
                { text: 'Sensor 1', value: 'T1' },
            ], "Zone"))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }

    toJsonLogic(node) {
        const zone = node.data.type1;

        return {
            "crowdDetection": zone
        }  
    }
}