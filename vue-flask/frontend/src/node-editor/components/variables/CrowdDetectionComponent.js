import Rete from "rete";
import * as Socket from "../../sockets";

import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";
import Node from "../../../../node_modules/rete-vue-render-plugin/src/variables/Node.vue";

export class CrowdDetectionComponent extends Rete.Component {
    constructor(){
        super("Crowd Detection");
        this.data.component = Node;
    }

    async builder(node) {

        const urlDesktop = "127.0.0.1:5000"
        const urlRasp = "192.168.1.216:5000"
        
        const responseZones = await fetch(`http://${urlDesktop}/sensors`);
        const sensors = await responseZones.json();

        let all = []


        for (let x in sensors) {

            let sensor = sensors[x]

            all.push(sensor.name);
            
        }

        let out1 = new Rete.Output('num', "Out", Socket.boolean);
        return node

            .addControl(new SelectControl(this.editor, 'type1', all.map((value) => ({
            text: `${value}`, value: `${value}`,
          })), "Zone"))
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