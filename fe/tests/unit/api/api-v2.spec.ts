import ApiV2 from '@/api/api-v2';


describe('ApiV2', () => {
  let api = new ApiV2('http://localhost:20000');

  test('version', async () => {
    const version_text = await api.version();
    const versions = version_text.split("-");
    const semantic_version = versions[0]
        .split(".")
        .map((x) => Number.parseInt(x));
    console.debug(`Version: ${semantic_version}`)
    expect(semantic_version.length).toEqual(3);
    expect(semantic_version[0]).toEqual(2);  // 2.x.x
    expect(semantic_version[1]).toBeGreaterThanOrEqual(0);
    expect(semantic_version[2]).toBeGreaterThanOrEqual(0);
  });
});
