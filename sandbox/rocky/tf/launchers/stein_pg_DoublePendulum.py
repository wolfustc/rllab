

from sandbox.rocky.tf.algos.pg_stein import PGStein
from rllab.envs.box2d.double_pendulum_env import DoublePendulumEnv
from rllab.baselines.linear_feature_baseline import LinearFeatureBaseline
from rllab.envs.normalized_env import normalize
from sandbox.rocky.tf.policies.gaussian_mlp_policy import GaussianMLPPolicy
from sandbox.rocky.tf.envs.base import TfEnv
from rllab.misc.instrument import stub, run_experiment_lite

stub(globals())

env = TfEnv(normalize(DoublePendulumEnv()))

policy = GaussianMLPPolicy(
    name="policy",
    env_spec=env.spec,
    hidden_sizes=(100, 50, 25),
    adaptive_std=True,
    std_hidden_sizes=(100,25),
)

baseline = LinearFeatureBaseline(env_spec=env.spec)

algo = PGStein(
    env=env,
    policy=policy,
    baseline=baseline,
    batch_size=10000,
    max_path_length=500,
    n_itr=100,
    discount=0.99,
    delta=0.01,
    optimizer_args=dict(
        batch_size=100,
        max_epochs=1,
        learning_rate=0.01,
        max_batch=100,
        alpha = 1,
        subsample_factor=0.1,
    )
)

run_experiment_lite(
    algo.train(),
    n_parallel=4,
    seed=1,
)
