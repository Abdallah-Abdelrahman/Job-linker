import { useLoginMutation, useRegisterMutation } from '../../app/services/auth';

function Register() {
  const [signup, { isLoading, isError, isSuccess }] = useRegisterMutation();

  const handleSubmit = (evt) => {
    evt.preventDefault();
    const form = new FormData(evt.currentTarget);
    signup(Object.fromEntries(form))
      .unwrap()
      .then(data => console.log({ data }))
      .catch(err => console.error({ err }))

  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        required
        type="text"
        name='name'
        placeholder="Name"
      />
      <input
        required
        type="email"
        name="email"
        placeholder="Email"
      />
      <input
        required
        type="password"
        name="password"
        placeholder="Password"
      />
      <select required name='role'>
        <option value="">Select role</option>
        <option value="candidate">Candidate</option>
        <option value="recruiter">Recruiter</option>
      </select>
      <button type="submit">Register</button>

    </form>
  )
}

export default Register;
