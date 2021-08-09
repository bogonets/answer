import ApiV2 from '@/apis/api-v2';

const DEFAULT_RECC_SERVER_ADDRESS = 'http://localhost:20000';

function getReccServerAddress(): string {
  return process.env.RECC_SERVER_ADDRESS || DEFAULT_RECC_SERVER_ADDRESS;
}

describe('ApiV2', () => {
  let api = new ApiV2(getReccServerAddress());

  test('version', async () => {
    const version_text = await api.getVersion();
    const versions = version_text.split("-");
    const semantic_version = versions[0]
        .split(".")
        .map((x) => Number.parseInt(x));
    expect(semantic_version.length).toEqual(3);
    expect(semantic_version[0]).toEqual(2);  // 2.x.x
    expect(semantic_version[1]).toBeGreaterThanOrEqual(0);
    expect(semantic_version[2]).toBeGreaterThanOrEqual(0);
  });

  test('heartbeat', async () => {
    let result: boolean | undefined = undefined;
    await api.getHeartbeat()
        .then(() => {
            result = true;
        })
        .catch(() => {
          result = false;
        });
    expect(result).toBeTruthy();
  });

  test('test_init', async () => {
    const result = await api.getTestInit();
    expect(typeof result).toEqual('boolean');
  });
});
