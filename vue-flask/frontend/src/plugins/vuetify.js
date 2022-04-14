import 'font-awesome/css/font-awesome.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'


import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

export default new Vuetify({
    icons: {
        iconfont: 'md' || 'fa'
      },
      theme: {
        themes: {
            light: {
                primary: colors.deepPurple.darken4, // #E53935
                secondary: colors.lightBlue.darken1, // #FFCDD2
                accent: colors.indigo.base, // #3F51B5
                background: colors.grey.lighten2, // Not automatically applied
              },
            dark: {
                background: colors.shades.white, // If not using lighten/darken, use base to return hex
            },
        },
      },
});