import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'

const Sessions = () => {
  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <Card>
          <CardHeader>
            <CardTitle>Sessions</CardTitle>
            <CardDescription>Manage your learning and teaching sessions</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">Sessions component coming soon...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Sessions

