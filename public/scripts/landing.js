const DOMAIN = 'boredgames.io'

class Landing extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      game_id: '',
      player_code: '',
      spymaster_code: '',
      // Initialize the two below to make the form a controlled input
      gameId: '',
      gameCode: ''
    }

    this.createGame = this.createGame.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.joinGame = this.joinGame.bind(this)
    this.onCreateGame = this.onCreateGame.bind(this)
    this.renderCreateForm = this.renderCreateForm.bind(this)
    this.renderJoinForm = this.renderJoinForm.bind(this)
  }

  createGame() {
    $.post({
      url: `http://${DOMAIN}/new_game`,
      success: this.onCreateGame
    })
  }

  handleChange(event) {
    if (event.target.name === 'gameId') {
      this.setState({ gameId: event.target.value })
    } else if (event.target.name === 'gameCode') {
      this.setState({ gameCode: event.target.value })
    }
  }

  joinGame(event) {
    event.preventDefault()
    const id = this.state.gameId
    const code = this.state.gameCode
    window.location.href = `http://${DOMAIN}/game?id=${id}&code=${code}`
  }

  onCreateGame(data) {
    this.setState({
      game_id: data.game_id,
      player_code: data.player_code,
      spymaster_code: data.spymaster_code
    })
  }

  renderCreateForm() {
    return (
      <table>
        <tbody>
          <tr>
            <td><h2>Create A Game</h2></td>
          </tr>
          <tr>
            <td>Game ID: </td>
            <td>{this.state.game_id}</td>
          </tr>
          <tr>
            <td>Player Code: </td>
            <td>{this.state.player_code}</td>
          </tr>
          <tr>
            <td>Spymaster Code: </td>
            <td>{this.state.spymaster_code}</td>
          </tr>
          <tr>
            <td><button onClick={this.createGame}>Create Game</button></td>
          </tr>
        </tbody>
      </table>
    )
  }

  renderJoinForm() {
    return(
      <form onSubmit={this.joinGame}>
        <table>
          <tbody>
            <tr>
              <td><h2>Join A Game</h2></td>
            </tr>
            <tr>
              <td>Game ID: </td>
              <td>
                <input type="text"
                       name="gameId"
                       value={this.state.gameId}
                       onChange={this.handleChange} />
              </td>
            </tr>
            <tr>
              <td>Game Code: </td>
              <td>
                <input type="text"
                       name="gameCode"
                       value={this.state.gameCode}
                       onChange={this.handleChange} />
              </td>
            </tr>
            <tr>
              <td><input type="submit" value="Join Game" /></td>
            </tr>
          </tbody>
        </table>
      </form>
    )
  }

  render() {
    const createForm = this.renderCreateForm()
    const joinForm = this.renderJoinForm()

    return(
      <div>
        {createForm}
        {joinForm}
      </div>
    )
  }
}

ReactDOM.render(
  <Landing />,
  document.getElementById('content')
)
