import ConnectionPlugin from "rete-connection-plugin";
import VueRenderPlugin from "rete-vue-render-plugin";
import ContextMenuPlugin from "rete-context-menu-plugin";
import AreaPlugin from "rete-area-plugin";
import KeyboardPlugin from 'rete-keyboard-plugin';

import router from '@/router'
import vuetify from '@/plugins/vuetify'

import { AddComponent } from '@/node-editor/components/AddComponent'
import { SubComponent } from '@/node-editor/components/SubComponent'
import { ANDComponent } from '@/node-editor/components/ANDComponent'
import { ConstantComponent } from '@/node-editor/components/ConstantComponent'
import { DifferentThanComponent } from '@/node-editor/components/DifferentThanComponent'
import { DivisionComponent } from '@/node-editor/components/DivisionComponent'
import { EqualToComponent } from '@/node-editor/components/EqualToComponent'
import { JamComponent } from '@/node-editor/components/JamComponent'
import { FlowComponent } from '@/node-editor/components/FlowComponent'
import { GreaterThanComponent } from '@/node-editor/components/GreaterThanComponent'
import { GreaterThanOrEqualToComponent } from '@/node-editor/components/GreaterThanOrEqualToComponent'
import { LessThanComponent } from '@/node-editor/components/LessThanComponent'
import { LessThanOrEqualToComponent } from '@/node-editor/components/LessThanOrEqualToComponent'
import { MultiplyComponent } from '@/node-editor/components/MultiplyComponent'
import { NOTComponent } from '@/node-editor/components/NOTComponent'
import { ORComponent } from '@/node-editor/components/ORComponent'
import { StayTimeComponent } from '@/node-editor/components/StayTimeComponent'
import { VehicleDetectionComponent } from '@/node-editor/components/VehicleDetectionComponent'
import { EndComponent } from '@/node-editor/components/EndComponent'
import { DurationComponent } from '@/node-editor/components/DurationComponent'
import { CrowdDetectionComponent } from '@/node-editor/components/CrowdDetectionComponent'
import { MaxComponent } from '@/node-editor/components/MaxComponent'
import { MinComponent } from '@/node-editor/components/MinComponent'


import Rete from "rete";


export default async function(container) {
    const components = [ new VehicleDetectionComponent(), new StayTimeComponent(), new FlowComponent(), 
        new JamComponent(), new CrowdDetectionComponent(), new AddComponent(), new SubComponent(), new MultiplyComponent(), new DivisionComponent(), new EqualToComponent(), 
        new DifferentThanComponent(), new MaxComponent(), new MinComponent(), new GreaterThanComponent(), new LessThanComponent(), new GreaterThanOrEqualToComponent(), new LessThanOrEqualToComponent(), 
        new ANDComponent(), new ORComponent(), new NOTComponent(), new DurationComponent(), new ConstantComponent(), new EndComponent()];
  
    const editor = new Rete.NodeEditor("demo@0.1.0", container);

    editor.use(ConnectionPlugin);
    editor.use(VueRenderPlugin, {
        options: {
          router,
          vuetify
        }
    });
    editor.use(ContextMenuPlugin);
    editor.use(AreaPlugin);
    editor.use(KeyboardPlugin);
  
    const engine = new Rete.Engine("demo@0.1.0");
  
    components.map(c => {
      editor.register(c);
      engine.register(c);
    });

    var n1 = await components[0].createNode({num: 2});
    var n2 = await components[0].createNode({num: 0});
    var add = await components[1].createNode();
    
    n1.position = [80, 200];
    n2.position = [80, 400];
    add.position = [500, 240];
  
    editor.on(
      "process nodecreated noderemoved connectioncreated connectionremoved",
      async () => {
        await engine.abort();
        await engine.process(editor.toJSON());
      }
    );
  
    editor.view.resize();
    AreaPlugin.zoomAt(editor);
    editor.trigger('process');

    return {
      editor
    }
  }
  
