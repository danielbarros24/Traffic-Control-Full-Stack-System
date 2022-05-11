import Rete from "rete";
import * as Socket from "../sockets";

export class FluxoComponent extends Rete.Component {
    constructor(){
        super("Fluxo");
    }

    builder(node) {
        
        var inp1 = new Rete.Input('str', "Zone", Socket.road);
        var inp2 = new Rete.Input('num', "Time", Socket.number);
        var out1 = new Rete.Output('Out', "Out", Socket.number);

        return node

          .addInput(inp1)
          .addInput(inp2)
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
}