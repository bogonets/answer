import {createLocalVue, mount} from '@vue/test-utils';
import Vuetify from 'vuetify';
import AppBarTitle from '@/components/AppBarTitle.vue';

describe('AppBarTitle.vue', () => {
  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Default rendering', () => {
    const testTitle = 'aaa';
    const testSubtitle = 'bbb';

    const wrapper = mount(AppBarTitle, {
      localVue,
      vuetify,
      propsData: {
        title: testTitle,
        subtitle: testSubtitle,
      },
    });

    expect(wrapper.props('title')).toMatch(testTitle);
    expect(wrapper.props('subtitle')).toMatch(testSubtitle);
    expect(wrapper.props('flat')).toBeFalsy();
    console.log(wrapper.html());
  });
});
