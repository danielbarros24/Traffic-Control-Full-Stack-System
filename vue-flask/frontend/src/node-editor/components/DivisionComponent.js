import Rete from "rete";
import * as Socket from "../sockets";

export class DivisionComponent extends Rete.Component {
    constructor(){
        super("/");
    }
    
    builder(node) {
        var inp1 = new Rete.Input('num1',"In", Socket.number, true);
        var out = new Rete.Output('num', "Out", Socket.number);

        return node
            .addInput(inp1)
            .addOutput(out);
    }
    
    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
}