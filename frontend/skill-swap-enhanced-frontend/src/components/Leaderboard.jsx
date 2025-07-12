import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'

const Leaderboard = () => {
  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <Card>
          <CardHeader>
            <CardTitle>Leaderboard</CardTitle>
            <CardDescription>See top performers in the SkillSwap community</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">Leaderboard component coming soon...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Leaderboard

