import 'font-awesome/css/font-awesome.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'


import Vue from 'vue';
import Vuetify from 'vuetify/lib';

import colors from 'vuetify/lib/util/colors'

// Translation provided by Vuetify (javascript)
import en from 'vuetify/lib/locale/en'

Vue.use(Vuetify);

export default new Vuetify({
    lang: {
      locales: { en },
      current: 'en',
    },
    icons: {
      iconfont: 'md' || 'fa'
    },
    theme: {
      themes: {
          light: {
              primary: colors.lightBlue.darken2, // #E53935
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
