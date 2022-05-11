import Rete from "rete";
import * as Socket from "../sockets";

export class TempoDePermanenciaComponent extends Rete.Component {
    constructor(){
        super("Tempo de permanência");
    }

    builder(node) {
        var inp1 = new Rete.Input('str', "Vehicle type", Socket.vehicle);
        var inp2 = new Rete.Input('num', "Zone", Socket.road);
        var out = new Rete.Output('num', "Out", Socket.number);

        return node

            .addInput(inp1)
            .addInput(inp2)
            .addOutput(out);
    }

    worker(node, outputs) {
        outputs['num'] = node.data.num;
    }
}