import { createRouter, createWebHistory } from 'vue-router';

import Home from './views/Home.vue';
import ChannelView from './views/ChannelView.vue';
import BroadcastPlayer from './views/BroadcastPlayer.vue';


const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,

    },
    {
        path: '/channel/:id',
        name: 'ChannelView',
        component: ChannelView,
        props: true,
    },
    {
        path: '/broadcast/:id',
        name: 'BroadcastPlayer',
        component: BroadcastPlayer,
        props: true,
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;