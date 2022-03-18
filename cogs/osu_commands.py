import discord
from discord.ext import commands
from ossapi import OssapiV2

osuapi = OssapiV2("client id", "client secret", "callback url")

class OsuCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def osu(self, ctx, userid):
        osu_user = osuapi.user(userid)
        embed = discord.Embed(
            title=f"Stats for {osu_user.username}", 
            type="rich", 
            url=f"https://osu.ppy.sh/users/{osu_user.id}"
        )
        embed.set_thumbnail(url=f'{osu_user.avatar_url}')
        embed.add_field(
            name="Performance:",
            value=f"""
                    --- **{osu_user.statistics.pp}pp**
                    **Global Rank:** #{osu_user.statistics.global_rank} ({osu_user.country_code}: #{osu_user.statistics.country_rank})
                    **Accuracy:** {osu_user.statistics.hit_accuracy:.2f}
                    **Play Count:** {osu_user.statistics.play_count}
                    **Level:** {osu_user.statistics.level.current}
                """
        )
        embed.add_field(
            name="Ranks:",
            value=f"""
                    SSH: {osu_user.statistics.grade_counts.ssh}
                    SS: {osu_user.statistics.grade_counts.ss}
                    SH: {osu_user.statistics.grade_counts.sh}
                    S: {osu_user.statistics.grade_counts.s}
                    A: {osu_user.statistics.grade_counts.a}
                """
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(OsuCommands(bot))
