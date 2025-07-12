import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'

const Notifications = () => {
  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <Card>
          <CardHeader>
            <CardTitle>Notifications</CardTitle>
            <CardDescription>Stay updated with your latest activities</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">Notifications component coming soon...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Notifications

