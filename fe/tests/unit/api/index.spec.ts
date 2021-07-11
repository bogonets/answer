import ApiV2 from '@/api';


describe('ApiV2', () => {
  let api = new ApiV2('http://localhost:20000');

  test('getVersion', async () => {
    const result = await api.getVersion();
    console.debug('Version: ' + result)
    expect(result.length).toBeGreaterThan(0);
  });
});
