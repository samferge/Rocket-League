from util.objects import *
from util.routines import *
from util.tools import find_hits

class Bot(GoslingAgent):
    # This function runs every in-game tick (every time the game updates anything)
    def run(self):
        self.print_debug()
        white= self.renderer.white()
        self.renderer.draw_line_3d(self.me.location, self.ball.location, white)
        if self.get_intent() is not None:
            self.debug_intent()
            return
        if self.time % 2 == 0:
            self.is_on_defense()
            self.rotate_back_post()
        if self.get_intent() is not None:
            return
        # Kickoff
        if self.kickoff_flag:
            self.set_intent(kickoff())
            return
        targets = {
            "at_opponent_goal": (self.foe_goal.left_post, self.foe_goal.right_post),"away_from_friend_goal": (self.friend_goal.right_post,self.friend_goal.left_post,),}
        my_boost_amount = self.me.boost
        closest_boost = self.get_closest_large_boost()

        hits = find_hits(self, targets)
        if self.is_in_front_of_ball() and self.is_on_defense():
            print("return to net")
            if self.at_goal():
                self.set_intent(hits["at_opponent_goal"][0])
                print("at opponent goal")
                return
            elif self.rotate_back_post() == "left":
                print("rotate back right post")
                self.set_intent(goto(self.friend_goal.left_post_rotation))
                return
            else:
                print("rotate back left post")

                self.set_intent(goto(self.friend_goal.right_post_rotation))
                return
        if (closest_boost is not None and my_boost_amount < 10 and not self.is_on_defense()):
            self.set_intent(goto(closest_boost.location))
            print("going for boost")
            return
        if len(hits["at_opponent_goal"]) > 0:
            self.set_intent(hits["at_opponent_goal"][0])
            print("at opponent goal")
            return
        if len(hits["away_from_friend_goal"]) > 0:
            self.set_intent(hits["away_from_friend_goal"][0])
            print("away from my goal")
            self.debug_text = 'getting boost'
            return