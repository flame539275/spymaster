class GameScore extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    const blueStyle = { color: '#3385FF' }
    const redStyle = { color: '#FF6666' }
    return(
      <table>
        <tbody className="score">
          <tr style={blueStyle}>
            <td>Blue Team</td>
            <td>{this.props.blueScore}</td>
          </tr>
          <tr style={redStyle}>
            <td>Red Team</td>
            <td>{this.props.redScore}</td>
          </tr>
        </tbody>
      </table>
    )
  }
}
