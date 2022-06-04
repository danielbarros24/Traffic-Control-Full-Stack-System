import Rete from "rete";
import * as Socket from "../../sockets";
import Node from "../../../../node_modules/rete-vue-render-plugin/src/logical-operators/Node.vue";

export class ORComponent extends Rete.Component {
    constructor(){
        super("OR");
        this.data.component = Node;
    }
    
    builder(node) {
        var inp1 = new Rete.Input('num1',"Inputs", Socket.boolean, true);
        var out = new Rete.Output('num', "Out", Socket.boolean);

        return node
            .addInput(inp1)
            .addOutput(out);
    }
    
    worker(node, outputs) {
        outputs['num'] = node.data.num;
    }

    toJsonLogic(node) {
        const { inputs } = node;
        
        const inputNum = inputs.get('num1');
        const { connections } = inputNum;

        return {
            "or": connections.map(connection => {
                const connectionNode = connection.output.node;
                const connectionComponent = this.editor.getComponent(connectionNode.name);
                return connectionComponent.toJsonLogic?.(connectionNode)
            })  
        }  
    }
}