import Rete from "rete";
import * as Socket from "../sockets";

export class FilaComponent extends Rete.Component {
    constructor(){
        super("Fila");
    }

    builder(node) {

        var inp1 = new Rete.Input('str', "Zone", Socket.road);
        var out1 = new Rete.Output('num', "Out", Socket.number);
        return node

          .addInput(inp1)
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
}